# Commercial Credit Stress Testing & Portfolio Risk Project

This repository is the scenario and stress-testing layer in the commercial credit-risk stack. It uses upstream PD, LGD, EAD, and expected loss style inputs together with defined downturn scenarios to produce stressed facility, segment, and portfolio loss views. The outputs are designed to support downstream pricing, monitoring, capital analysis, and lending strategy review in a clear portfolio-project format.

## What this repo is

This project demonstrates how a commercial lending portfolio can be stress tested once the core risk component outputs already exist. It is structured as a recruiter-friendly workflow with transparent scenario assumptions, reproducible code, and reporting outputs that are easy to interpret across both institutional portfolio review and non-bank portfolio management.

## Where it sits in the stack

Upstream inputs:
- `industry-analysis`
- `PD-and-scorecard-commercial`
- `LGD-commercial`
- `EAD-CCF-commercial`
- `expected-loss-engine-commercial`

Downstream consumers:
- `RAROC-pricing-and-return-hurdle`
- `portfolio-monitor-commercial`
- `RWA-capital-commercial`

## How this is used in practice

This project can be applied in:

### Bank / Institutional context

- Portfolio stress testing for downturn review, risk appetite discussion, and capital-style analysis
- Segment and product stress views for structured portfolio risk assessment
- Scenario overlays for management packs and stress-based monitoring

### Non-bank / Fintech context

- Approval strategy and pricing review under adverse scenarios
- Portfolio performance stress views by cohort, segment, or product
- Early risk planning for funding, collections, and growth decisions under downside assumptions

## Example input datasets

- `data/raw/demo_upstream_risk_inputs.csv`: sample facility-level upstream risk dataset with PD, LGD, EAD, expected loss, collateral, industry, and maturity fields.
- `data/external/stress_scenarios.csv`: reusable scenario table covering Base, Mild downturn, and Severe downturn assumptions.

## Key outputs

- `outputs/tables/stress_scenario_results.csv`
- `outputs/tables/pd_stress_uplift.csv`
- `outputs/tables/lgd_stress_uplift.csv`
- `outputs/tables/ead_stress_uplift.csv`
- `outputs/tables/stress_loss_dashboard_inputs.csv`
- `outputs/tables/stressed_expected_loss_by_facility.csv`
- `outputs/tables/stressed_expected_loss_by_segment.csv`
- `outputs/tables/portfolio_stress_summary.csv`
- `outputs/tables/validation_report.csv`

## Example outputs

- `outputs/tables/portfolio_stress_summary.csv`: portfolio-level comparison of base versus stressed EAD and expected loss by scenario.
- `outputs/tables/stressed_expected_loss_by_segment.csv`: segment view showing which borrower groups absorb the largest downturn uplift.
- `outputs/tables/stress_loss_dashboard_inputs.csv`: reporting-ready table for charting scenario results in dashboards or presentation packs.
- `outputs/reports/stress_testing_run_summary.md`: run summary with validation checks and generated file references.
- `outputs/charts/portfolio_stressed_el_by_scenario.png`: chart showing expected loss movement across scenarios.
- `outputs/charts/segment_stressed_el_severe_downturn.png`: chart highlighting segment concentrations in the severe scenario.
- `outputs/samples/sample_portfolio_stress_summary.csv`: lightweight sample for quick review without rerunning the pipeline.

## End-to-end workflow

1. Load the facility-level upstream demo dataset and scenario table.
2. Validate required fields, duplicate structure, and scenario definitions.
3. Apply scenario multipliers to PD, LGD, EAD, collateral values, and recovery timing.
4. Recalculate stressed expected loss for each facility under each scenario.
5. Aggregate results to facility, segment, and portfolio outputs.
6. Write tables, charts, sample outputs, and a validation summary to `outputs/`.

## Example business use case

A portfolio manager wants to understand how a severe downturn would affect commercial property, SME, and agribusiness exposures before repricing or capital review. This repo makes that easy to show: the reviewer can open `portfolio_stress_summary.csv`, trace the uplift into `stressed_expected_loss_by_segment.csv`, and see which segments drive the change.

## How these outputs feed downstream repos

- `RAROC-pricing-and-return-hurdle`: uses `outputs/tables/portfolio_stress_summary.csv` and `outputs/tables/stress_loss_dashboard_inputs.csv` as “stress context” for pricing and hurdle discussion.
- `portfolio-monitor-commercial`: can reuse `outputs/tables/stress_loss_dashboard_inputs.csv` as scenario inputs for monitoring packs and early-warning overlays.
- `RWA-capital-commercial`: can reuse `outputs/tables/portfolio_stress_summary.csv` and facility/segment stress tables as the stress leg of capital reporting.

## Repo structure

- `data/`: raw, processed, and external stress scenario inputs
- `src/`: reusable scenario, stress engine, validation, and reporting modules
- `scripts/`: pipeline entry-point wrappers
- `docs/`: methodology, assumptions, data dictionary, and validation notes
- `notebooks/`: walkthrough notebooks for reviewer context
- `outputs/`: exported tables, charts, reports, and sample artifacts
- `tests/`: validation and regression checks

## How to run

Quick start:

```powershell
pip install -r requirements.txt
python scripts/run_pipeline.py
```

After the run, start with:

- `outputs/reports/stress_testing_run_summary.md`
- `outputs/tables/portfolio_stress_summary.csv`
- `outputs/charts/portfolio_stressed_el_by_scenario.png`

Run validation tests:

```powershell
python -m pytest
```

## Testing and validation

- `tests/test_stress_pipeline.py` checks that demo inputs pass validation before the engine runs.
- The test suite confirms scenario ordering, so Severe downturn produces higher expected loss than Mild downturn, and Mild downturn is above Base.
- Base scenario outputs are checked against upstream components to confirm that unstressed PD, LGD, and EAD are preserved.
- Facility-level stressed outputs are reconciled back to the portfolio summary, and the generated `outputs/tables/validation_report.csv` records the same validation logic in a reviewer-friendly format.

## Limitations / Demo-Only Note

- All data is synthetic and is provided for demonstration only.
- Scenario multipliers and overlays are illustrative rather than macro-model calibrated.
- The repo is intended to show workflow design and reporting quality, not to represent a live bank stress-testing framework.
