# Plan 07 evidence review

Aggregate evidence from [retained analysis run 37406368550](https://github.com/jschell/rsd407-pay/actions/runs/37406368550).

Regenerate with `PYTHONPATH=src python -m rsd407_pay.access_extract_reconcile`, then `PYTHONPATH=src python scripts/review_plan07.py` from the repository root after downloading that run’s artifact into `artifacts/`. Input hashes and complete numeric comparisons are in [the machine-readable evidence](evidence/plan07-review.json).

## Access-to-extract reconciliation

All twelve years match employee-row counts and base salary, total salary, insurance, mandatory benefits, and employer compensation exactly. Maximum FTE difference is 9.870000212686136e-07 FTE, within the existing Access verifier’s 0.000001 FTE allowance. This is a same-S-275-system cross-check, not independent validation. Component certificated/classified FTE are not separately registered in the accepted controls.

## Warning review

These employee-year rows remain in the source totals. The table quantifies the effect of zero-FTE rows on total salary; the salary gap is base minus total among salary-below-base rows, not a demonstrated underpayment. Conditions can overlap. Counts are employee-year rows, not distinct people across twelve years.

| Year | Zero-FTE rows | Their total salary | Share of annual salary | Salary below base rows | Aggregate base-minus-total gap |
|---|---:|---:|---:|---:|---:|
| 2013-14 | 11 | $61,262 | 0.33% | 12 | $99,459 |
| 2014-15 | 17 | $148,854 | 0.78% | 15 | $116,665 |
| 2015-16 | 29 | $202,382 | 0.97% | 22 | $171,516 |
| 2016-17 | 25 | $272,229 | 1.22% | 19 | $128,353 |
| 2017-18 | 27 | $216,351 | 0.91% | 19 | $118,962 |
| 2018-19 | 27 | $221,104 | 0.84% | 19 | $143,051 |
| 2019-20 | 29 | $215,208 | 0.77% | 28 | $163,154 |
| 2020-21 | 29 | $103,432 | 0.37% | 29 | $271,724 |
| 2021-22 | 31 | $234,211 | 0.76% | 24 | $230,308 |
| 2022-23 | 36 | $252,532 | 0.80% | 35 | $407,634 |
| 2023-24 | 30 | $288,130 | 0.89% | 54 | $961,739 |
| 2024-25 | 2 | $4,586 | 0.01% | 27 | $207,580 |

The PR source-warning job replays the retained SHA-identified Access databases and checks these four diagnostics against normalized results in every year. Its output establishes whether the conditions originate in the reporting source; it does not establish individual payroll explanations. No compensation is imputed or silently removed.

## Annual changes

The following decomposes flagged nominal increases into recorded components. Neither this accounting decomposition nor passing reconciliation establishes a cause such as a contract change.

| Period | Measure | Increase | Percent | Components |
|---|---|---:|---:|---|
| 2017-18 to 2018-19 | base_salary | $4,186,919 | 22.63% | base_salary: $4,186,919 |
| 2017-18 to 2018-19 | reported_employer_compensation | $5,352,203 | 17.76% | total_salary: $2,617,281; insurance_benefits: $2,125,446; mandatory_benefits: $609,476 |
| 2023-24 to 2024-25 | reported_employer_compensation | $6,487,916 | 15.27% | total_salary: $3,898,832; insurance_benefits: $2,082,768; mandatory_benefits: $506,316 |

The JSON also includes exact job-family contributions and FTE-versus-compensation-per-FTE growth for each change.

## Independent published controls

Personnel Summary Table 45B FTE and base salary pass for all six available years, 2019-20 through 2024-25. Exact published comparisons, source hashes, and display-rounding bounds are preserved in the JSON; reviewed pages and literal compensation rows are in `controls/personnel-summary-published.json`.

Total salary, insurance, and mandatory benefits remain unresolved semantic comparisons. In 2024-25, the extract is $2,828,198.43 below implied published total salary, $233,409.07 below insurance, and $483,813.76 below mandatory benefits. These are material limitations. They are not given arbitrary tolerances or represented as independently validated. The exact match with Access supports faithful simplified-extract aggregation, not equivalence with every published measure.

Annual independent published control coverage for 2013-14 through 2018-19 remains unavailable. Those years pass internal and same-system checks only.

## Closeout boundary

Plan 07 remains active until the new source-warning corroboration and complete PR analysis pass and the source-condition limitations are accepted in the completion record. No claim of payroll correctness, independent twelve-year compensation validation, or explanation of individual compensation is made.
