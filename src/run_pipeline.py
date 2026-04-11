"""Run the stress-testing pipeline end to end."""

from __future__ import annotations

from pathlib import Path

from .config import DEFAULT_PORTFOLIO_PATH, DEFAULT_SCENARIO_PATH
from .engine import apply_stress_scenarios
from .loaders import load_inputs
from .outputs import (
    build_output_tables,
    write_charts,
    write_output_tables,
    write_run_report,
)
from .validation import (
    build_validation_dataframe,
    format_validation_report,
    reconcile_facility_to_portfolio,
    validate_portfolio_input,
    validate_scenario_table,
    validate_stress_results,
)


def run_pipeline(
    portfolio_path: str | Path = DEFAULT_PORTFOLIO_PATH,
    scenario_path: str | Path = DEFAULT_SCENARIO_PATH,
) -> dict[str, Path]:
    """Run input loading, stress calculations, validation, and output generation."""

    portfolio, scenarios = load_inputs(portfolio_path, scenario_path)

    validate_portfolio_input(portfolio)
    validate_scenario_table(scenarios)

    stress_results = apply_stress_scenarios(portfolio, scenarios)
    validation_checks = validate_stress_results(stress_results)

    tables = build_output_tables(stress_results, scenarios)
    validation_checks.extend(
        reconcile_facility_to_portfolio(
            tables["facility_results"],
            tables["portfolio_summary"],
        )
    )
    tables["validation_report"] = build_validation_dataframe(validation_checks)
    validation_report = format_validation_report(validation_checks)

    output_paths = write_output_tables(tables)
    output_paths.update(write_charts(tables))
    output_paths["run_report"] = write_run_report(validation_report, output_paths)
    return output_paths


def main() -> None:
    output_paths = run_pipeline()
    print("Stress-testing pipeline completed.")
    for key, path in sorted(output_paths.items()):
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
