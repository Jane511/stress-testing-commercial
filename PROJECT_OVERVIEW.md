# Project Overview - stress-testing-commercial

## Purpose

`stress-testing-commercial` is a modular Australian credit-risk portfolio demonstration. It shows how a bank-style commercial portfolio can be stressed once upstream PD, LGD, EAD, and Expected Loss outputs already exist.

## Repository Role

This repository is a downstream scenario overlay engine. It does not rebuild scorecards, LGD models, or CCF models. Instead, it merges upstream-style outputs and applies practical scenario overlays for:

- PD uplift
- LGD uplift
- EAD or utilisation uplift
- collateral value haircut
- recovery delay

## Portfolio Demonstration Scope

The synthetic portfolio includes SME, commercial, agribusiness, and property-related facilities across multiple Australian industries and states. The outputs are designed to show:

- facility-level stressed loss movement
- segment-level portfolio stress impact
- concentration effects by segment and industry
- scenario comparison from base to severe downturn

## Employer Review Angle

The repository is structured for employer review:

- reproducible Python pipeline
- clear documentation and assumptions
- public or synthetic inputs only
- GitHub-ready outputs and notebooks
- simple validation and reconciliation checks

## Downstream Use

The outputs are positioned to feed:

- `RAROC-pricing-and-return-hurdle`
- `Portfolio-Monitoring-MIS`
- `RWA-capital-commercial`
