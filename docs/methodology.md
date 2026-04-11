# Methodology

## Objective

The stress-testing engine measures how credit portfolio risk changes when base risk components are stressed under defined downturn scenarios.

The engine starts with facility-level upstream outputs:

- base PD
- base LGD
- base EAD
- base Expected Loss

It then applies transparent scenario overlays and recalculates stressed Expected Loss.

## Core Formula

Base Expected Loss:

```text
base_expected_loss = base_pd x base_lgd x base_ead
```

Stressed Expected Loss:

```text
stressed_expected_loss = stressed_pd x stressed_lgd x stressed_ead
```

## PD Stress Method

Stressed PD is calculated from:

```text
stressed_pd = base_pd x scenario_pd_multiplier x industry_overlay x property_overlay x concentration_overlay
```

The engine caps stressed PD at 99 percent to avoid impossible values.

Industry overlays are applied only when the scenario enables them. More cyclical industries such as construction, retail trade, accommodation and food services, and transport receive stronger PD overlays than more defensive industries.

Property overlays are applied where a facility is property-secured or property-sensitive and the scenario includes property-market softness.

Concentration overlays are applied when a segment or industry has a high share of portfolio EAD.

## LGD Stress Method

Stressed LGD is calculated from:

```text
stressed_lgd = base_lgd x scenario_lgd_multiplier
             + collateral_haircut_addon
             + recovery_delay_addon
             + property_softness_addon
```

The engine caps stressed LGD at 95 percent.

Collateral haircuts increase LGD more for facilities with higher collateral dependency. Recovery delays increase LGD through a simple monthly delay add-on. Property-market softness adds an additional LGD overlay to property-secured exposures in downturn scenarios.

## EAD Stress Method

Stressed EAD is calculated from:

```text
stressed_ead = base_ead x scenario_ead_multiplier + stressed_drawdown_on_undrawn_commitments
```

The result is capped at the facility current limit. Revolving or working-capital products receive a higher drawdown overlay than amortising term products.

## Aggregation

The pipeline aggregates results by:

- facility
- borrower
- segment
- product
- industry
- portfolio

Portfolio-level PD and LGD metrics are EAD-weighted averages. Expected Loss is summed.

## Outputs

The output tables are designed for dashboarding and downstream portfolio analysis. Facility-level files keep the detailed stressed components, while segment and portfolio files provide decision-ready summary views.

