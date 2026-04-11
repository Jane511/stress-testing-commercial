# stress-testing-commercial

## 1. What this repo is

This repository is a bank-style Australian credit-risk stress testing module for a commercial lending portfolio demonstration. It applies transparent scenario overlays to upstream Probability of Default (PD), Loss Given Default (LGD), Exposure at Default (EAD), and Expected Loss outputs, then shows portfolio impact clearly at facility, segment, and total portfolio level.

The repository is intentionally employer-friendly. It demonstrates portfolio stress testing workflow, reproducible code structure, and practical reporting outputs without overstating model complexity.

## 2. Where it sits in the full credit-risk stack

`stress-testing-commercial` is the public GitHub repo for the portfolio stress-testing layer.

Upstream inputs:

- `industry-analysis`
- `PD-and-scorecard-commercial`
- `LGD-commercial`
- `EAD-CCF-commercial`
- `expected-loss-engine-commercial`

Those upstream components provide the base risk inputs. This repo applies scenarios to those upstream components rather than building separate PD, LGD, or EAD models from scratch.

Downstream consumers:

- `RAROC-pricing-and-return-hurdle`
- `Portfolio-Monitoring-MIS`
- `RWA-capital-commercial`

## 3. Inputs

The pipeline uses a facility-level upstream-style dataset with:

- facility and borrower identifiers
- segment, product, industry, and state
- base PD, LGD, EAD, and Expected Loss
- outstanding balance, undrawn amount, current limit, and collateral value
- a property security flag
- an `upstream_source` field showing the conceptual source component

Included demo inputs:

- `data/raw/demo_upstream_risk_inputs.csv`
- `data/external/stress_scenarios.csv`

All included data is public-style synthetic demo data.

## 4. What the pipeline does

The pipeline:

1. Loads synthetic upstream-style facility outputs and scenario assumptions.
2. Standardises columns and validates input completeness.
3. Applies base, mild downturn, and severe downturn overlays.
4. Stresses PD, LGD, EAD, collateral values, and recovery timing using simple explainable formulas.
5. Recalculates stressed Expected Loss.
6. Aggregates stressed results by facility, segment, industry, and portfolio.
7. Produces reporting-ready CSV tables, sample extracts, charts, and a validation report.

## 5. Outputs

Required output tables are written to `outputs/tables/`:

- `stress_scenario_results.csv`
- `pd_stress_uplift.csv`
- `lgd_stress_uplift.csv`
- `ead_stress_uplift.csv`
- `stress_loss_dashboard_inputs.csv`

Additional reviewer-friendly outputs include:

- `stressed_expected_loss_by_facility.csv`
- `stressed_expected_loss_by_segment.csv`
- `portfolio_stress_summary.csv`
- `portfolio_concentration_summary.csv`
- `validation_report.csv`

Supporting artefacts are also written to:

- `outputs/charts/`
- `outputs/reports/`
- `outputs/samples/`

## 6. How to run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the stress-testing pipeline:

```bash
python scripts/run_pipeline.py
```

Run validation tests:

```bash
python -m pytest
```

Open the notebooks in sequence for a walkthrough:

```bash
jupyter notebook notebooks/
```

## 7. Limitations and synthetic-data note

This repository uses synthetic demo data only. It does not use confidential bank data and should be read as a portfolio demonstration rather than a production stress testing framework.

Practical limitations:

- scenario multipliers are illustrative rather than macro-model calibrated
- collateral haircuts and recovery delays are simplified overlays
- concentration effects are rule-based
- the module assumes upstream base PD, LGD, EAD, and Expected Loss values already exist

## 8. How it connects to the next repo

The stressed outputs are designed to pass into downstream pricing, monitoring, and capital views:

- `RAROC-pricing-and-return-hurdle` can use stressed loss and exposure metrics for pricing sensitivity
- `Portfolio-Monitoring-MIS` can use scenario outputs for dashboarding and concentration views
- `RWA-capital-commercial` can use stressed EAD and loss views for capital sensitivity analysis
