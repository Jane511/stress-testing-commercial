"""Core stress engine for scenario overlays and portfolio aggregation."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import LGD_CAP, PD_CAP
from .features import (
    add_concentration_flags,
    collateral_dependency,
    concentration_pd_overlay,
    drawdown_factor,
    industry_pd_overlay,
    property_lgd_overlay,
    property_pd_overlay,
)


def apply_stress_scenarios(portfolio: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    """Apply all configured scenarios to facility-level upstream inputs."""

    portfolio = add_concentration_flags(portfolio)
    stressed_frames: list[pd.DataFrame] = []

    for _, scenario in scenarios.iterrows():
        scenario_df = portfolio.copy()
        scenario_name = scenario["scenario_name"]

        scenario_df["scenario_name"] = scenario_name
        scenario_df["scenario_notes"] = scenario["notes"]
        scenario_df["scenario_pd_multiplier"] = scenario["pd_multiplier"]
        scenario_df["scenario_lgd_multiplier"] = scenario["lgd_multiplier"]
        scenario_df["scenario_ead_multiplier"] = scenario["ead_multiplier"]
        scenario_df["collateral_haircut_pct"] = scenario["collateral_haircut_pct"]
        scenario_df["recovery_delay_months"] = scenario["recovery_delay_months"]

        scenario_df["industry_overlay_factor"] = scenario_df["industry"].apply(
            lambda value: industry_pd_overlay(value, scenario_name, bool(scenario["industry_overlay_flag"]))
        )
        scenario_df["property_pd_overlay_factor"] = scenario_df["property_secured_flag"].apply(
            lambda value: property_pd_overlay(
                bool(value),
                scenario_name,
                bool(scenario["property_market_softness_flag"]),
            )
        )
        scenario_df["concentration_overlay_factor"] = scenario_df.apply(
            lambda row: concentration_pd_overlay(
                bool(row["segment_concentration_flag"]),
                bool(row["industry_concentration_flag"]),
                scenario_name,
                bool(scenario["concentration_overlay_flag"]),
            ),
            axis=1,
        )

        scenario_df["stressed_pd"] = (
            scenario_df["base_pd"]
            * scenario["pd_multiplier"]
            * scenario_df["industry_overlay_factor"]
            * scenario_df["property_pd_overlay_factor"]
            * scenario_df["concentration_overlay_factor"]
        ).clip(lower=0.0, upper=PD_CAP)

        dependency = collateral_dependency(scenario_df["base_ead"], scenario_df["collateral_value"])
        scenario_df["collateral_haircut_lgd_addon"] = scenario["collateral_haircut_pct"] * dependency * 0.35
        scenario_df["recovery_delay_lgd_addon"] = scenario["recovery_delay_months"] * 0.0025
        scenario_df["property_lgd_addon"] = scenario_df["property_secured_flag"].apply(
            lambda value: property_lgd_overlay(
                bool(value),
                scenario_name,
                bool(scenario["property_market_softness_flag"]),
            )
        )
        scenario_df["stressed_lgd"] = (
            scenario_df["base_lgd"] * scenario["lgd_multiplier"]
            + scenario_df["collateral_haircut_lgd_addon"]
            + scenario_df["recovery_delay_lgd_addon"]
            + scenario_df["property_lgd_addon"]
        ).clip(lower=0.0, upper=LGD_CAP)

        scenario_df["drawdown_factor"] = scenario_df["product"].apply(
            lambda value: drawdown_factor(value, scenario_name)
        )
        raw_stressed_ead = (
            scenario_df["base_ead"] * scenario["ead_multiplier"]
            + scenario_df["undrawn_amount"] * scenario_df["drawdown_factor"]
        )
        scenario_df["stressed_ead"] = np.minimum(raw_stressed_ead, scenario_df["current_limit"]).clip(lower=0.0)

        scenario_df["base_expected_loss"] = (
            scenario_df["base_pd"] * scenario_df["base_lgd"] * scenario_df["base_ead"]
        )
        scenario_df["stressed_expected_loss"] = (
            scenario_df["stressed_pd"] * scenario_df["stressed_lgd"] * scenario_df["stressed_ead"]
        )
        scenario_df["incremental_expected_loss"] = (
            scenario_df["stressed_expected_loss"] - scenario_df["base_expected_loss"]
        )

        scenario_df["pd_uplift_pct"] = _safe_uplift(scenario_df["stressed_pd"], scenario_df["base_pd"])
        scenario_df["lgd_uplift_pct"] = _safe_uplift(scenario_df["stressed_lgd"], scenario_df["base_lgd"])
        scenario_df["ead_uplift_pct"] = _safe_uplift(scenario_df["stressed_ead"], scenario_df["base_ead"])
        scenario_df["expected_loss_uplift_pct"] = _safe_uplift(
            scenario_df["stressed_expected_loss"],
            scenario_df["base_expected_loss"],
        )
        stressed_frames.append(scenario_df)

    return pd.concat(stressed_frames, ignore_index=True)


def aggregate_results(results: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    """Aggregate facility-level outputs and calculate weighted portfolio metrics."""

    rows = []
    for group_values, group in results.groupby(group_columns, dropna=False):
        if not isinstance(group_values, tuple):
            group_values = (group_values,)

        base_ead_total = group["base_ead"].sum()
        stressed_ead_total = group["stressed_ead"].sum()
        row = dict(zip(group_columns, group_values))
        row.update(
            {
                "facility_count": group["facility_id"].nunique(),
                "borrower_count": group["borrower_id"].nunique(),
                "base_ead": base_ead_total,
                "stressed_ead": stressed_ead_total,
                "base_expected_loss": group["base_expected_loss"].sum(),
                "stressed_expected_loss": group["stressed_expected_loss"].sum(),
                "incremental_expected_loss": group["incremental_expected_loss"].sum(),
                "base_pd_weighted": _weighted_average(group["base_pd"], group["base_ead"]),
                "stressed_pd_weighted": _weighted_average(group["stressed_pd"], group["stressed_ead"]),
                "base_lgd_weighted": _weighted_average(group["base_lgd"], group["base_ead"]),
                "stressed_lgd_weighted": _weighted_average(group["stressed_lgd"], group["stressed_ead"]),
            }
        )
        row["expected_loss_uplift_pct"] = (
            row["stressed_expected_loss"] / row["base_expected_loss"] - 1
            if row["base_expected_loss"] > 0
            else 0.0
        )
        rows.append(row)

    return pd.DataFrame(rows)


def portfolio_summary(results: pd.DataFrame) -> pd.DataFrame:
    """Return portfolio-level stress results by scenario."""

    summary = aggregate_results(results, ["scenario_name"])
    return summary.sort_values("stressed_expected_loss").reset_index(drop=True)


def concentration_summary(results: pd.DataFrame) -> pd.DataFrame:
    """Return simple concentration views by segment and industry."""

    segment = aggregate_results(results, ["scenario_name", "segment"])
    segment["concentration_view"] = "segment"
    segment["concentration_name"] = segment["segment"]

    industry = aggregate_results(results, ["scenario_name", "industry"])
    industry["concentration_view"] = "industry"
    industry["concentration_name"] = industry["industry"]

    combined = pd.concat([segment, industry], ignore_index=True, sort=False)
    return combined.sort_values(
        ["scenario_name", "concentration_view", "stressed_expected_loss"],
        ascending=[True, True, False],
    )


def _safe_uplift(stressed: pd.Series, base: pd.Series) -> pd.Series:
    with np.errstate(divide="ignore", invalid="ignore"):
        uplift = (stressed / base) - 1
    return uplift.replace([np.inf, -np.inf], np.nan).fillna(0.0)


def _weighted_average(values: pd.Series, weights: pd.Series) -> float:
    if weights.sum() <= 0:
        return 0.0
    return float(np.average(values, weights=weights))
