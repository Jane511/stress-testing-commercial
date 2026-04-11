import pandas as pd

from src.engine import apply_stress_scenarios
from src.loaders import load_portfolio, load_scenarios
from src.outputs import build_output_tables
from src.validation import (
    reconcile_facility_to_portfolio,
    validate_portfolio_input,
    validate_scenario_table,
    validate_stress_results,
)


def test_demo_inputs_pass_validation():
    portfolio = load_portfolio()
    scenarios = load_scenarios()

    validate_portfolio_input(portfolio)
    validate_scenario_table(scenarios)


def test_severe_scenario_increases_expected_loss():
    portfolio = load_portfolio()
    scenarios = load_scenarios()
    results = apply_stress_scenarios(portfolio, scenarios)

    totals = results.groupby("scenario_name")["stressed_expected_loss"].sum()

    assert totals["Severe downturn"] > totals["Mild downturn"]
    assert totals["Mild downturn"] > totals["Base"]


def test_base_scenario_preserves_upstream_components():
    portfolio = load_portfolio()
    scenarios = load_scenarios()
    results = apply_stress_scenarios(portfolio, scenarios)
    base = results[results["scenario_name"] == "Base"]

    pd.testing.assert_series_equal(
        base["base_pd"].reset_index(drop=True),
        base["stressed_pd"].reset_index(drop=True),
        check_names=False,
    )
    pd.testing.assert_series_equal(
        base["base_lgd"].reset_index(drop=True),
        base["stressed_lgd"].reset_index(drop=True),
        check_names=False,
    )
    pd.testing.assert_series_equal(
        base["base_ead"].reset_index(drop=True),
        base["stressed_ead"].reset_index(drop=True),
        check_names=False,
    )


def test_output_reconciliation():
    portfolio = load_portfolio()
    scenarios = load_scenarios()
    results = apply_stress_scenarios(portfolio, scenarios)
    tables = build_output_tables(results, scenarios)

    checks = validate_stress_results(results)
    checks.extend(
        reconcile_facility_to_portfolio(
            tables["facility_results"],
            tables["portfolio_summary"],
        )
    )

    assert len(checks) >= 6
