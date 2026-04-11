Create a new repo: stress-testing-commercial

Goal:
Build a bank-style credit stress-testing repository for my Australian credit-risk portfolio.

Purpose:
This repo must apply stress scenarios to upstream risk components and show the impact on:
- PD
- LGD
- EAD
- Expected Loss
- segment risk
- portfolio risk

This repo is a downstream scenario engine.
It should not rebuild PD, LGD, EAD, or Expected Loss from scratch.
Instead, it must consume outputs from upstream repos.

Upstream dependencies:
- industry-analysis
- PD-and-scorecard-commercial
- LGD-commercial
- EAD-CCF-commercial
- expected-loss-engine-commercial

Main objective:
Create a professional, employer-ready GitHub repository that demonstrates how stress testing can be performed on an Australian lending portfolio using public or synthetic portfolio data.

Working style:
- Be practical, not overly academic
- Use Python + notebooks + markdown + CSV outputs
- Keep code modular and readable
- Use realistic assumptions where internal bank data would normally be needed
- Keep everything reproducible for a public GitHub portfolio
- Do not invent hidden dependencies
- Do not use broken local paths or legacy local folder references
- Make the repo clean enough for recruiters and hiring managers to review

Required repo structure:
stress-testing-commercial/
├── README.md
├── PROJECT_OVERVIEW.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── notebooks/
│   ├── 00_data_prep.ipynb
│   ├── 01_scenario_design.ipynb
│   ├── 02_stress_engine.ipynb
│   ├── 03_validation.ipynb
│   └── 04_reporting.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── loaders.py
│   ├── scenarios.py
│   ├── stress_engine.py
│   ├── validation.py
│   ├── outputs.py
│   └── run_pipeline.py
├── scripts/
│   └── run_pipeline.py
├── outputs/
│   ├── tables/
│   ├── charts/
│   ├── reports/
│   └── samples/
├── docs/
│   ├── methodology.md
│   ├── assumptions.md
│   ├── data_dictionary.md
│   └── validation_framework.md
└── tests/

README requirements:
Write a strong, practical README using this order:
1. What this repo is
2. Where it sits in the full credit-risk stack
3. Inputs
4. What the pipeline does
5. Stress scenarios covered
6. Outputs
7. How to run
8. Limitations / synthetic-data note
9. How it connects to downstream repos

README positioning:
The README should clearly say:
- this is a bank-style stress-testing portfolio project
- it applies scenario overlays to PD, LGD, EAD, and Expected Loss
- it is for educational and portfolio purposes
- it is not a live production stress-testing framework
- it sits downstream of the core risk component repos

Required documentation files:
Create and populate:
- PROJECT_OVERVIEW.md
- docs/methodology.md
- docs/assumptions.md
- docs/data_dictionary.md
- docs/validation_framework.md

Scenario design requirements:
Build at least 3 scenarios:
1. Base
2. Mild downturn
3. Severe downturn

Stress dimensions to include:
- PD uplift
- LGD uplift
- EAD / utilisation uplift
- collateral value haircut
- recovery delay
- sector-specific overlay where appropriate
- property-market softness overlay where appropriate
- concentration sensitivity by segment or industry where practical

Scenario framework requirements:
Create a reusable scenario table that contains:
- scenario_name
- pd_multiplier
- lgd_multiplier
- ead_multiplier
- collateral_haircut_pct
- recovery_delay_months
- industry_overlay_flag
- notes

Pipeline requirements:
Build code and notebooks that:
1. load upstream sample outputs or synthetic demo inputs
2. standardise the required input fields
3. apply scenario multipliers and stress overlays
4. recalculate stressed PD, stressed LGD, stressed EAD
5. recalculate stressed expected loss
6. aggregate stressed results by:
   - facility
   - borrower
   - segment
   - product
   - industry
   - portfolio
7. export reporting-ready CSV outputs
8. generate a few simple charts and summary tables

Core logic expectations:
- stressed_PD = base_PD adjusted by scenario uplift and segment overlays
- stressed_LGD = base_LGD adjusted by downturn, collateral haircut, and recovery assumptions
- stressed_EAD = base_EAD adjusted by utilisation / drawdown assumptions
- stressed_EL = stressed_PD × stressed_LGD × stressed_EAD

Required output files:
- stress_scenario_results.csv
- pd_stress_uplift.csv
- lgd_stress_uplift.csv
- ead_stress_uplift.csv
- stressed_expected_loss_by_facility.csv
- stressed_expected_loss_by_segment.csv
- stress_loss_dashboard_inputs.csv
- portfolio_stress_summary.csv

Sample output expectations:
Include small demo output files in outputs/samples so a reviewer can understand the repo without running a full dataset.

Validation requirements:
Create validation logic and documentation covering:
- input completeness checks
- duplicate record checks
- scenario table validation
- reasonableness checks on uplift factors
- comparison of base vs stressed outputs
- simple sensitivity checks
- reconciliation from facility totals to portfolio totals

Notebook expectations:
- notebooks should explain the logic clearly
- notebooks should be suitable for portfolio demonstration
- keep notebook outputs clean unless useful as examples
- reusable logic must live in src/, not only inside notebooks

Coding standards:
- use clear variable names
- add comments
- include input/output validation
- keep functions modular
- avoid overengineering
- keep everything readable for non-technical credit reviewers as well

Data assumptions:
Where real internal stress data is unavailable:
- use synthetic or illustrative portfolio data
- clearly label assumptions
- keep assumptions realistic for Australian SME and property-related lending
- document which fields are illustrative

Downstream use:
The README must explicitly state that this repo feeds:
- RAROC-pricing-and-return-hurdle
- portfolio-monitor-commercial (planned downstream repo; not yet published on the public portfolio)
- RWA-capital-commercial

Important clean-up rules:
- remove any outdated numbered-repo wording
- do not use local Windows-only paths
- do not leave placeholder text like “todo”
- do not leave broken imports or empty notebooks
- make the repo feel complete

Expected final response from Codex:
At the end, provide:
1. the final repo tree
2. a summary of all files created or changed
3. a short explanation of the stress-testing logic
4. sample outputs created
5. remaining future enhancements
