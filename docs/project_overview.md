# Project Overview

`stress-testing-commercial` is the downstream scenario and stress-testing engine in the public commercial credit-risk stack.

## Portfolio role

It applies scenario overlays to upstream PD, LGD, EAD, and expected-loss outputs to produce stressed facility, segment, and portfolio views.

## Upstream inputs

- `industry-analysis`
- `PD-and-scorecard-commercial`
- `LGD-commercial`
- `EAD-CCF-commercial`
- `expected-loss-engine-commercial`

## Downstream consumers

- `RAROC-pricing-and-return-hurdle`
- `portfolio-monitor-commercial`
- `RWA-capital-commercial`
