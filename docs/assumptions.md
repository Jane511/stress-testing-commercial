# Assumptions

## Data Assumptions

The included portfolio is synthetic and illustrative. It is designed to resemble Australian SME, commercial, agribusiness, working-capital, equipment-finance, and property-related lending, but it is not sourced from a real bank.

Illustrative fields include:

- base PD
- base LGD
- base EAD
- base Expected Loss
- collateral value
- undrawn amount
- current limit
- score band
- arrears status
- refinance maturity

## Scenario Assumptions

The scenario table includes three scenarios:

- Base
- Mild downturn
- Severe downturn

The scenario assumptions are transparent and deliberately simple:

- PD rises under economic stress.
- LGD rises when collateral values weaken and recoveries take longer.
- EAD rises where borrowers draw more of their available limits.
- Property-secured and property-sensitive exposures are more affected by property-market softness.
- Cyclical industries receive higher PD overlays.
- concentrated segments or industries receive an additional sensitivity overlay.

## Australian Portfolio Context

The assumptions reflect common Australian lending risk themes:

- property collateral is important for SME and commercial lending recoveries
- construction and property-related exposures can be sensitive to valuation changes and refinancing conditions
- working-capital and overdraft products may see higher utilisation in downturns
- agriculture, retail, transport, and hospitality can be cyclical

## Model Boundaries

This project does not estimate macroeconomic transition models, default correlations, capital requirements, or regulatory stress test submissions. It is a practical scenario overlay engine for public portfolio demonstration.

## Governance Assumptions

In a production bank environment, assumptions would require independent model validation, data lineage checks, approval by risk governance forums, and regular back-testing. This public portfolio version documents assumptions directly in code and markdown for transparency.

