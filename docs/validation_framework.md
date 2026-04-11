# Validation Framework

## Validation Objectives

The validation framework is designed to confirm that:

- input data is complete enough to run the stress engine
- scenario assumptions are reasonable
- stressed outputs are internally consistent
- facility-level results reconcile to portfolio-level summaries

## Input Completeness Checks

The portfolio input must contain all required facility, borrower, product, industry, exposure, collateral, and base risk fields.

Required checks:

- missing required columns
- null values in required columns
- non-numeric values in numeric fields
- negative exposure values
- PD and LGD values outside the 0 to 1 range

## Duplicate Record Checks

`facility_id` must be unique in the input portfolio. Duplicate facility records are treated as a data quality error because they can overstate exposure and Expected Loss.

## Scenario Table Validation

The scenario table must include:

- scenario name
- PD multiplier
- LGD multiplier
- EAD multiplier
- collateral haircut percentage
- recovery delay months
- overlay flags
- notes

Reasonableness ranges are applied to prevent accidental extreme inputs. For example, multipliers must be positive, collateral haircuts must be between 0 and 50 percent, and recovery delay assumptions must be non-negative.

## Output Reasonableness Checks

The engine checks that:

- stressed PD remains between 0 and 99 percent
- stressed LGD remains between 0 and 95 percent
- stressed EAD is non-negative
- stressed Expected Loss is non-negative
- the severe scenario produces higher portfolio Expected Loss than the base scenario

## Base Versus Stressed Comparison

The base scenario is expected to preserve upstream PD, LGD, EAD, and Expected Loss. Mild and severe downturn scenarios should show the incremental effect of scenario overlays.

## Sensitivity Checks

Simple sensitivity checks compare:

- Base versus mild downturn
- Base versus severe downturn
- Mild downturn versus severe downturn
- segment-level incremental Expected Loss

These checks are designed to highlight whether the direction of stress is sensible.

## Reconciliation Checks

Facility-level stressed Expected Loss must reconcile to portfolio-level stressed Expected Loss for each scenario. The same reconciliation is performed for base Expected Loss.

