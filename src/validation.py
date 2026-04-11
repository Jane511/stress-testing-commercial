"""Validation checks for inputs and stress outputs."""

from __future__ import annotations

import pandas as pd

from .config import (
    LGD_CAP,
    NUMERIC_PORTFOLIO_COLUMNS,
    PD_CAP,
    REQUIRED_PORTFOLIO_COLUMNS,
    REQUIRED_SCENARIO_COLUMNS,
)


def _missing_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    return [column for column in required_columns if column not in df.columns]


def validate_portfolio_input(portfolio: pd.DataFrame) -> None:
    """Raise ValueError if the portfolio input is incomplete or unreasonable."""

    missing = _missing_columns(portfolio, REQUIRED_PORTFOLIO_COLUMNS)
    if missing:
        raise ValueError(f"Portfolio input is missing required columns: {missing}")

    null_columns = [
        column
        for column in REQUIRED_PORTFOLIO_COLUMNS
        if portfolio[column].isna().any()
    ]
    if null_columns:
        raise ValueError(f"Portfolio input has null values in required columns: {null_columns}")

    duplicate_ids = portfolio.loc[portfolio["facility_id"].duplicated(), "facility_id"].tolist()
    if duplicate_ids:
        raise ValueError(f"Duplicate facility_id values found: {duplicate_ids}")

    for column in NUMERIC_PORTFOLIO_COLUMNS:
        if column in portfolio.columns and not pd.api.types.is_numeric_dtype(portfolio[column]):
            raise ValueError(f"Portfolio column must be numeric: {column}")

    non_negative_columns = [
        "outstanding_balance",
        "undrawn_amount",
        "current_limit",
        "collateral_value",
        "base_ead",
        "base_expected_loss",
    ]
    for column in non_negative_columns:
        if (portfolio[column] < 0).any():
            raise ValueError(f"Portfolio column contains negative values: {column}")

    if not portfolio["base_pd"].between(0, 1).all():
        raise ValueError("base_pd must be between 0 and 1")
    if not portfolio["base_lgd"].between(0, 1).all():
        raise ValueError("base_lgd must be between 0 and 1")
    if (portfolio["current_limit"] < portfolio["outstanding_balance"]).any():
        raise ValueError("current_limit cannot be below outstanding_balance")


def validate_scenario_table(scenarios: pd.DataFrame) -> None:
    """Raise ValueError if the scenario table is incomplete or unreasonable."""

    missing = _missing_columns(scenarios, REQUIRED_SCENARIO_COLUMNS)
    if missing:
        raise ValueError(f"Scenario table is missing required columns: {missing}")

    if scenarios["scenario_name"].isna().any():
        raise ValueError("Scenario names cannot be null")
    if scenarios["scenario_name"].duplicated().any():
        raise ValueError("Scenario names must be unique")

    required_scenarios = {"base", "mild downturn", "severe downturn"}
    scenario_names = {value.strip().lower() for value in scenarios["scenario_name"]}
    if not required_scenarios.issubset(scenario_names):
        raise ValueError("Scenario table must include Base, Mild downturn, and Severe downturn")

    multiplier_columns = ["pd_multiplier", "lgd_multiplier", "ead_multiplier"]
    for column in multiplier_columns:
        if scenarios[column].isna().any() or (scenarios[column] <= 0).any():
            raise ValueError(f"{column} must be positive and non-null")
        if (scenarios[column] > 3).any():
            raise ValueError(f"{column} contains an implausibly high multiplier")

    if not scenarios["collateral_haircut_pct"].between(0, 0.5).all():
        raise ValueError("collateral_haircut_pct must be between 0 and 0.5")
    if not scenarios["recovery_delay_months"].between(0, 24).all():
        raise ValueError("recovery_delay_months must be between 0 and 24")


def validate_stress_results(results: pd.DataFrame) -> list[str]:
    """Validate stress outputs and return human-readable check results."""

    checks: list[str] = []

    if not results["stressed_pd"].between(0, PD_CAP).all():
        raise ValueError("stressed_pd contains values outside the configured cap")
    checks.append("PASS: stressed_pd values are within configured bounds.")

    if not results["stressed_lgd"].between(0, LGD_CAP).all():
        raise ValueError("stressed_lgd contains values outside the configured cap")
    checks.append("PASS: stressed_lgd values are within configured bounds.")

    if (results["stressed_ead"] < 0).any():
        raise ValueError("stressed_ead contains negative values")
    checks.append("PASS: stressed_ead values are non-negative.")

    if (results["stressed_expected_loss"] < 0).any():
        raise ValueError("stressed_expected_loss contains negative values")
    checks.append("PASS: stressed_expected_loss values are non-negative.")

    base_rows = results[results["scenario_name"].str.lower() == "base"]
    if not base_rows.empty:
        max_base_difference = (
            base_rows["stressed_expected_loss"] - base_rows["base_expected_loss"]
        ).abs().max()
        if max_base_difference > 0.01:
            raise ValueError("Base scenario does not reconcile to base Expected Loss")
        checks.append("PASS: Base scenario reconciles to upstream Expected Loss.")

    scenario_totals = (
        results.groupby("scenario_name", as_index=False)["stressed_expected_loss"].sum()
    )
    totals_by_name = {
        row["scenario_name"].lower(): row["stressed_expected_loss"]
        for _, row in scenario_totals.iterrows()
    }
    if "base" in totals_by_name and "severe downturn" in totals_by_name:
        if totals_by_name["severe downturn"] <= totals_by_name["base"]:
            raise ValueError("Severe downturn Expected Loss should exceed base Expected Loss")
        checks.append("PASS: Severe downturn increases portfolio Expected Loss versus base.")

    return checks


def reconcile_facility_to_portfolio(
    facility_results: pd.DataFrame,
    portfolio_summary: pd.DataFrame,
    tolerance: float = 0.01,
) -> list[str]:
    """Check that facility-level totals reconcile to portfolio-level summaries."""

    facility_totals = (
        facility_results.groupby("scenario_name", as_index=False)
        .agg(
            facility_base_expected_loss=("base_expected_loss", "sum"),
            facility_stressed_expected_loss=("stressed_expected_loss", "sum"),
        )
    )
    merged = facility_totals.merge(portfolio_summary, on="scenario_name", how="left")

    base_diff = (
        merged["facility_base_expected_loss"] - merged["base_expected_loss"]
    ).abs()
    stressed_diff = (
        merged["facility_stressed_expected_loss"] - merged["stressed_expected_loss"]
    ).abs()

    if (base_diff > tolerance).any() or (stressed_diff > tolerance).any():
        raise ValueError("Facility-level results do not reconcile to portfolio summary")

    return [
        "PASS: Facility-level base Expected Loss reconciles to portfolio summary.",
        "PASS: Facility-level stressed Expected Loss reconciles to portfolio summary.",
    ]


def format_validation_report(checks: list[str]) -> str:
    """Format validation checks for a markdown report."""

    lines = ["# Stress Testing Validation Report", ""]
    lines.extend(f"- {check}" for check in checks)
    return "\n".join(lines) + "\n"


def build_validation_dataframe(checks: list[str]) -> pd.DataFrame:
    """Return validation checks in tabular form for downstream review."""

    rows = []
    for check in checks:
        status, message = check.split(": ", maxsplit=1)
        rows.append({"status": status, "check": message})
    return pd.DataFrame(rows)
