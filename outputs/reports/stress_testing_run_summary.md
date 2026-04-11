# Stress Testing Run Summary

## Validation

- PASS: stressed_pd values are within configured bounds.
- PASS: stressed_lgd values are within configured bounds.
- PASS: stressed_ead values are non-negative.
- PASS: stressed_expected_loss values are non-negative.
- PASS: Base scenario reconciles to upstream Expected Loss.
- PASS: Severe downturn increases portfolio Expected Loss versus base.
- PASS: Facility-level base Expected Loss reconciles to portfolio summary.
- PASS: Facility-level stressed Expected Loss reconciles to portfolio summary.

## Generated Files

- `concentration_summary`: `outputs\tables\portfolio_concentration_summary.csv`
- `dashboard_inputs`: `outputs\tables\stress_loss_dashboard_inputs.csv`
- `ead_uplift`: `outputs\tables\ead_stress_uplift.csv`
- `facility_results`: `outputs\tables\stressed_expected_loss_by_facility.csv`
- `lgd_uplift`: `outputs\tables\lgd_stress_uplift.csv`
- `pd_uplift`: `outputs\tables\pd_stress_uplift.csv`
- `portfolio_chart`: `outputs\charts\portfolio_stressed_el_by_scenario.png`
- `portfolio_summary`: `outputs\tables\portfolio_stress_summary.csv`
- `sample_portfolio_stress_summary.csv`: `outputs\samples\sample_portfolio_stress_summary.csv`
- `sample_stress_loss_dashboard_inputs.csv`: `outputs\samples\sample_stress_loss_dashboard_inputs.csv`
- `sample_stressed_expected_loss_by_segment.csv`: `outputs\samples\sample_stressed_expected_loss_by_segment.csv`
- `scenario_results`: `outputs\tables\stress_scenario_results.csv`
- `segment_chart`: `outputs\charts\segment_stressed_el_severe_downturn.png`
- `segment_results`: `outputs\tables\stressed_expected_loss_by_segment.csv`
- `validation_report`: `outputs\tables\validation_report.csv`
