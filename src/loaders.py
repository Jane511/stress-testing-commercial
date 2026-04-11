"""Input loading and schema standardisation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import (
    DEFAULT_PORTFOLIO_PATH,
    DEFAULT_SCENARIO_PATH,
    NUMERIC_PORTFOLIO_COLUMNS,
    OPTIONAL_SCENARIO_FLAG_COLUMNS,
)


def _snake_case_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def _parse_bool_series(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map({"true": True, "false": False, "1": True, "0": False, "yes": True, "no": False})
        .fillna(False)
        .astype(bool)
    )


def standardise_portfolio_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Return a clean portfolio DataFrame with predictable column names and types."""

    df = _snake_case_columns(df)

    for column in NUMERIC_PORTFOLIO_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype(float)

    if "property_secured_flag" in df.columns:
        df["property_secured_flag"] = _parse_bool_series(df["property_secured_flag"])

    if {"base_pd", "base_lgd", "base_ead"}.issubset(df.columns):
        calculated_el = df["base_pd"] * df["base_lgd"] * df["base_ead"]
        if "base_expected_loss" not in df.columns:
            df["base_expected_loss"] = calculated_el
        else:
            df["base_expected_loss"] = df["base_expected_loss"].fillna(calculated_el)

    return df


def standardise_scenario_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Return a clean scenario DataFrame with boolean flags and numeric assumptions."""

    df = _snake_case_columns(df)

    numeric_columns = [
        "pd_multiplier",
        "lgd_multiplier",
        "ead_multiplier",
        "collateral_haircut_pct",
        "recovery_delay_months",
    ]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    for column in ["industry_overlay_flag", *OPTIONAL_SCENARIO_FLAG_COLUMNS]:
        if column not in df.columns:
            df[column] = False
        df[column] = _parse_bool_series(df[column])

    return df


def load_portfolio(path: str | Path = DEFAULT_PORTFOLIO_PATH) -> pd.DataFrame:
    """Load the upstream facility-level risk component output."""

    portfolio = pd.read_csv(path)
    return standardise_portfolio_schema(portfolio)


def load_scenarios(path: str | Path = DEFAULT_SCENARIO_PATH) -> pd.DataFrame:
    """Load the reusable stress scenario table."""

    scenarios = pd.read_csv(path)
    return standardise_scenario_schema(scenarios)


def load_inputs(
    portfolio_path: str | Path = DEFAULT_PORTFOLIO_PATH,
    scenario_path: str | Path = DEFAULT_SCENARIO_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load portfolio and scenario inputs together."""

    return load_portfolio(portfolio_path), load_scenarios(scenario_path)
