"""Output builders and writers for stress-testing artefacts."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .config import CHARTS_DIR, OUTPUT_FILE_NAMES, REPORTS_DIR, SAMPLES_DIR, TABLES_DIR
from .engine import aggregate_results, concentration_summary, portfolio_summary

FACILITY_OUTPUT_COLUMNS = [
    "scenario_name",
    "facility_id",
    "borrower_id",
    "segment",
    "product",
    "industry",
    "state",
    "base_pd",
    "stressed_pd",
    "base_lgd",
    "stressed_lgd",
    "base_ead",
    "stressed_ead",
    "base_expected_loss",
    "stressed_expected_loss",
    "incremental_expected_loss",
    "pd_uplift_pct",
    "lgd_uplift_pct",
    "ead_uplift_pct",
    "expected_loss_uplift_pct",
    "industry_overlay_factor",
    "property_pd_overlay_factor",
    "concentration_overlay_factor",
    "collateral_haircut_lgd_addon",
    "recovery_delay_lgd_addon",
    "property_lgd_addon",
    "drawdown_factor",
]


def ensure_output_directories() -> None:
    for directory in [TABLES_DIR, CHARTS_DIR, REPORTS_DIR, SAMPLES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def build_output_tables(
    stress_results: pd.DataFrame,
    scenarios: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Build reporting tables used by outputs and validation."""

    facility_results = stress_results[FACILITY_OUTPUT_COLUMNS].copy()
    segment_results = aggregate_results(stress_results, ["scenario_name", "segment"]).sort_values(
        ["scenario_name", "segment"]
    )
    dashboard_inputs = aggregate_results(
        stress_results,
        ["scenario_name", "segment", "product", "industry"],
    ).sort_values(["scenario_name", "segment", "product", "industry"])
    summary = portfolio_summary(stress_results)
    concentration = concentration_summary(stress_results)

    scenario_results = summary.merge(scenarios, on="scenario_name", how="left")

    return {
        "scenario_results": scenario_results,
        "pd_uplift": facility_results[
            [
                "scenario_name",
                "facility_id",
                "borrower_id",
                "segment",
                "industry",
                "base_pd",
                "stressed_pd",
                "pd_uplift_pct",
                "industry_overlay_factor",
                "property_pd_overlay_factor",
                "concentration_overlay_factor",
            ]
        ],
        "lgd_uplift": facility_results[
            [
                "scenario_name",
                "facility_id",
                "segment",
                "product",
                "base_lgd",
                "stressed_lgd",
                "lgd_uplift_pct",
                "collateral_haircut_lgd_addon",
                "recovery_delay_lgd_addon",
                "property_lgd_addon",
            ]
        ],
        "ead_uplift": facility_results[
            [
                "scenario_name",
                "facility_id",
                "segment",
                "product",
                "base_ead",
                "stressed_ead",
                "ead_uplift_pct",
                "drawdown_factor",
            ]
        ],
        "facility_results": facility_results,
        "segment_results": segment_results,
        "dashboard_inputs": dashboard_inputs,
        "portfolio_summary": summary,
        "concentration_summary": concentration,
        "validation_report": pd.DataFrame(),
    }


def write_output_tables(tables: dict[str, pd.DataFrame]) -> dict[str, Path]:
    """Write required CSV outputs and sample extracts."""

    ensure_output_directories()
    written_paths: dict[str, Path] = {}

    for key, table in tables.items():
        output_path = TABLES_DIR / OUTPUT_FILE_NAMES[key]
        table.to_csv(output_path, index=False)
        written_paths[key] = output_path

    sample_map = {
        "sample_portfolio_stress_summary.csv": tables["portfolio_summary"],
        "sample_stressed_expected_loss_by_segment.csv": tables["segment_results"],
        "sample_stress_loss_dashboard_inputs.csv": tables["dashboard_inputs"],
    }
    for file_name, table in sample_map.items():
        sample_path = SAMPLES_DIR / file_name
        table.head(12).to_csv(sample_path, index=False)
        written_paths[file_name] = sample_path

    return written_paths


def write_charts(tables: dict[str, pd.DataFrame]) -> dict[str, Path]:
    """Generate simple charts for the stress reporting pack."""

    ensure_output_directories()
    chart_paths: dict[str, Path] = {}

    summary = tables["portfolio_summary"].copy()
    summary = summary.sort_values("stressed_expected_loss")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(summary["scenario_name"], summary["stressed_expected_loss"], color="#2f6f73")
    ax.set_title("Portfolio Stressed Expected Loss By Scenario")
    ax.set_ylabel("Expected Loss")
    ax.set_xlabel("Scenario")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    path = CHARTS_DIR / "portfolio_stressed_el_by_scenario.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths["portfolio_chart"] = path

    segment = tables["segment_results"]
    severe = segment[segment["scenario_name"].str.lower() == "severe downturn"].copy()
    if not severe.empty:
        severe = severe.sort_values("stressed_expected_loss", ascending=True)
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.barh(severe["segment"], severe["stressed_expected_loss"], color="#85603f")
        ax.set_title("Severe Downturn Expected Loss By Segment")
        ax.set_xlabel("Expected Loss")
        ax.set_ylabel("Segment")
        fig.tight_layout()
        path = CHARTS_DIR / "segment_stressed_el_severe_downturn.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        chart_paths["segment_chart"] = path

    return chart_paths


def write_run_report(validation_report: str, output_paths: dict[str, Path]) -> Path:
    """Write a concise markdown report for the latest pipeline run."""

    ensure_output_directories()
    report_path = REPORTS_DIR / "stress_testing_run_summary.md"
    output_lines = ["# Stress Testing Run Summary", "", "## Validation", ""]
    output_lines.extend(validation_report.strip().splitlines()[2:])
    output_lines.extend(["", "## Generated Files", ""])

    for key, path in sorted(output_paths.items()):
        relative_path = path.relative_to(path.parents[2])
        output_lines.append(f"- `{key}`: `{relative_path}`")

    report_path.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    return report_path
