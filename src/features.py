"""Scenario feature engineering and overlay assumptions."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import CONCENTRATION_SHARE_THRESHOLD

REVOLVING_PRODUCTS = {
    "commercial credit card",
    "invoice finance",
    "overdraft",
    "working capital line",
}

INDUSTRY_PD_OVERLAYS = {
    "accommodation and food services": {"mild": 1.12, "severe": 1.35},
    "agriculture": {"mild": 1.08, "severe": 1.18},
    "construction": {"mild": 1.15, "severe": 1.35},
    "healthcare and social assistance": {"mild": 1.02, "severe": 1.05},
    "manufacturing": {"mild": 1.07, "severe": 1.18},
    "professional services": {"mild": 1.04, "severe": 1.10},
    "property services": {"mild": 1.12, "severe": 1.28},
    "retail trade": {"mild": 1.10, "severe": 1.25},
    "transport postal and warehousing": {"mild": 1.09, "severe": 1.22},
    "wholesale trade": {"mild": 1.08, "severe": 1.20},
}

PROPERTY_PD_OVERLAY = {"base": 1.00, "mild": 1.05, "severe": 1.12}
PROPERTY_LGD_ADDON = {"base": 0.00, "mild": 0.02, "severe": 0.06}
DRAWDOWN_FACTORS = {"base": 0.00, "mild": 0.10, "severe": 0.25}
CONCENTRATION_PD_OVERLAY = {"base": 1.00, "mild": 1.03, "severe": 1.08}


def scenario_severity(scenario_name: str) -> str:
    """Map a scenario name to a severity bucket."""

    name = str(scenario_name).strip().lower()
    if "severe" in name:
        return "severe"
    if "mild" in name:
        return "mild"
    return "base"


def add_concentration_flags(
    portfolio: pd.DataFrame,
    threshold: float = CONCENTRATION_SHARE_THRESHOLD,
) -> pd.DataFrame:
    """Add segment and industry concentration flags using base EAD share."""

    df = portfolio.copy()
    total_ead = df["base_ead"].sum()
    if total_ead <= 0:
        df["segment_ead_share"] = 0.0
        df["industry_ead_share"] = 0.0
    else:
        df["segment_ead_share"] = df.groupby("segment")["base_ead"].transform("sum") / total_ead
        df["industry_ead_share"] = df.groupby("industry")["base_ead"].transform("sum") / total_ead

    df["segment_concentration_flag"] = df["segment_ead_share"] >= threshold
    df["industry_concentration_flag"] = df["industry_ead_share"] >= threshold
    return df


def industry_pd_overlay(industry: str, scenario_name: str, enabled: bool) -> float:
    """Return a scenario-specific industry PD factor."""

    if not enabled:
        return 1.0
    severity = scenario_severity(scenario_name)
    if severity == "base":
        return 1.0
    return INDUSTRY_PD_OVERLAYS.get(str(industry).strip().lower(), {}).get(severity, 1.0)


def property_pd_overlay(property_secured: bool, scenario_name: str, enabled: bool) -> float:
    """Return a property-related PD factor."""

    if not enabled or not property_secured:
        return 1.0
    return PROPERTY_PD_OVERLAY[scenario_severity(scenario_name)]


def property_lgd_overlay(property_secured: bool, scenario_name: str, enabled: bool) -> float:
    """Return a property-related LGD add-on."""

    if not enabled or not property_secured:
        return 0.0
    return PROPERTY_LGD_ADDON[scenario_severity(scenario_name)]


def concentration_pd_overlay(
    segment_concentrated: bool,
    industry_concentrated: bool,
    scenario_name: str,
    enabled: bool,
) -> float:
    """Return a PD factor for concentrated pockets of the portfolio."""

    if not enabled or not (segment_concentrated or industry_concentrated):
        return 1.0
    return CONCENTRATION_PD_OVERLAY[scenario_severity(scenario_name)]


def drawdown_factor(product: str, scenario_name: str) -> float:
    """Return additional drawdown factor for revolving facilities."""

    if str(product).strip().lower() not in REVOLVING_PRODUCTS:
        return 0.0
    return DRAWDOWN_FACTORS[scenario_severity(scenario_name)]


def collateral_dependency(base_ead: pd.Series, collateral_value: pd.Series) -> pd.Series:
    """Estimate the share of EAD that behaves as collateral-dependent."""

    with np.errstate(divide="ignore", invalid="ignore"):
        coverage = collateral_value / base_ead.replace(0, np.nan)
    return coverage.fillna(0.0).clip(lower=0.0, upper=1.0)
