# Data Dictionary

## Input Fields

| Field | Description |
| --- | --- |
| `facility_id` | Unique facility identifier. |
| `borrower_id` | Borrower identifier used for borrower-level aggregation. |
| `segment` | Portfolio segment such as SME, Commercial, Agribusiness, or Commercial Property. |
| `product` | Lending product type. |
| `industry` | Borrower industry classification. |
| `state` | Australian state or territory. |
| `outstanding_balance` | Current drawn balance. |
| `undrawn_amount` | Available undrawn commitment. |
| `current_limit` | Current approved facility limit. |
| `collateral_value` | Illustrative collateral value available to support recovery. |
| `base_pd` | Upstream probability of default estimate. |
| `base_lgd` | Upstream loss given default estimate. |
| `base_ead` | Upstream exposure at default estimate. |
| `base_expected_loss` | Upstream base expected loss. |
| `property_secured_flag` | Indicates property-secured or property-sensitive exposure. |
| `score_band` | Illustrative scorecard or rating band. |
| `arrears_status` | Current arrears status. |
| `refinance_maturity_months` | Months until refinancing or major maturity event. |
| `upstream_source` | Name of upstream engine that produced the base risk components. |

## Scenario Fields

| Field | Description |
| --- | --- |
| `scenario_name` | Scenario label. |
| `pd_multiplier` | Scenario-level PD multiplier. |
| `lgd_multiplier` | Scenario-level LGD multiplier. |
| `ead_multiplier` | Scenario-level EAD multiplier. |
| `collateral_haircut_pct` | Collateral value haircut used in LGD stress. |
| `recovery_delay_months` | Additional recovery delay used in LGD stress. |
| `industry_overlay_flag` | Enables industry-specific PD overlays. |
| `property_market_softness_flag` | Enables property-market PD and LGD overlays. |
| `concentration_overlay_flag` | Enables concentration sensitivity overlays. |
| `notes` | Plain-English scenario description. |

## Output Fields

| Field | Description |
| --- | --- |
| `stressed_pd` | PD after scenario and overlay adjustments. |
| `stressed_lgd` | LGD after scenario and overlay adjustments. |
| `stressed_ead` | EAD after scenario and drawdown adjustments. |
| `stressed_expected_loss` | Recalculated expected loss under stress. |
| `incremental_expected_loss` | Difference between stressed and base Expected Loss. |
| `pd_uplift_pct` | Percentage uplift from base PD. |
| `lgd_uplift_pct` | Percentage uplift from base LGD. |
| `ead_uplift_pct` | Percentage uplift from base EAD. |
| `expected_loss_uplift_pct` | Percentage uplift from base Expected Loss. |

