"""Project paths and shared configuration."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

OUTPUTS_DIR = ROOT_DIR / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
CHARTS_DIR = OUTPUTS_DIR / "charts"
REPORTS_DIR = OUTPUTS_DIR / "reports"
SAMPLES_DIR = OUTPUTS_DIR / "samples"

DEFAULT_PORTFOLIO_PATH = RAW_DATA_DIR / "demo_upstream_risk_inputs.csv"
DEFAULT_SCENARIO_PATH = EXTERNAL_DATA_DIR / "stress_scenarios.csv"

REQUIRED_PORTFOLIO_COLUMNS = [
    "facility_id",
    "borrower_id",
    "segment",
    "product",
    "industry",
    "state",
    "outstanding_balance",
    "undrawn_amount",
    "current_limit",
    "collateral_value",
    "base_pd",
    "base_lgd",
    "base_ead",
    "base_expected_loss",
    "property_secured_flag",
    "upstream_source",
]

NUMERIC_PORTFOLIO_COLUMNS = [
    "outstanding_balance",
    "undrawn_amount",
    "current_limit",
    "collateral_value",
    "base_pd",
    "base_lgd",
    "base_ead",
    "base_expected_loss",
]

REQUIRED_SCENARIO_COLUMNS = [
    "scenario_name",
    "pd_multiplier",
    "lgd_multiplier",
    "ead_multiplier",
    "collateral_haircut_pct",
    "recovery_delay_months",
    "industry_overlay_flag",
    "property_market_softness_flag",
    "concentration_overlay_flag",
    "notes",
]

OPTIONAL_SCENARIO_FLAG_COLUMNS = [
    "property_market_softness_flag",
    "concentration_overlay_flag",
]

PD_CAP = 0.99
LGD_CAP = 0.95
CONCENTRATION_SHARE_THRESHOLD = 0.25

OUTPUT_FILE_NAMES = {
    "scenario_results": "stress_scenario_results.csv",
    "pd_uplift": "pd_stress_uplift.csv",
    "lgd_uplift": "lgd_stress_uplift.csv",
    "ead_uplift": "ead_stress_uplift.csv",
    "dashboard_inputs": "stress_loss_dashboard_inputs.csv",
    "facility_results": "stressed_expected_loss_by_facility.csv",
    "segment_results": "stressed_expected_loss_by_segment.csv",
    "portfolio_summary": "portfolio_stress_summary.csv",
    "concentration_summary": "portfolio_concentration_summary.csv",
    "validation_report": "validation_report.csv",
}
