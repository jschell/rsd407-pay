# Evaluation of nearby district administration, 2024-25

The available evidence supports a finding of higher strict central-administration compensation per student than nearby larger districts. It does not establish excessive compensation, excessive staffing, or inefficiency. Classification and school-count choices materially affect comparisons.

## Enrollment-size peers

2024-25 student FTE within +/-30% of Riverview; selected ten-district cohort only. The six peers are Sultan, Lakewood, Granite Falls, Tukwila, Orting, Steilacoom Historical.

| Classification | Riverview / 1,000 student FTE | Six-peer median / 1,000 | Riverview difference |
| --- | --- | --- | --- |
| Strict central administration | $404,596 | $419,450 | -3.5% |
| Strict plus every Director/Supervisor (scenario) | $1,026,531 | $891,287 | +15.2% |

Riverview is not above the size-peer median on the strict measure. Including every Director/Supervisor reverses that relation. Actual functional allocation is required before describing a complete central-office cost.

## Nearby larger districts

| District | Riverview strict cost difference | Staffing-intensity component of dollar gap / 1,000 | Compensation-per-FTE component | Riverview difference with all directors |
| --- | --- | --- | --- | --- |
| Snoqualmie Valley | +23.0% | $68,557 | $7,155 | +134.1% |
| Northshore | +37.2% | $125,723 | $-15,999 | +80.6% |
| Monroe | +58.0% | $140,743 | $7,834 | +55.1% |

The components divide the observed strict cost gap symmetrically between staffing per student and compensation per admin FTE. They are an arithmetic decomposition, not causal estimates. For Northshore, Riverview has lower compensation per admin FTE; higher staffing per student accounts for the positive cost gap.

## School-count sensitivity

OSPI school-type codes distinguish P (Public School), A (Alternative), S (Special Education), and R (Reengagement). See the [official data dictionary](https://data.wa.gov/education/Washington-School-Improvement-Framework-WSIF-2024-/8v2t-vz3j). The denominator check below retains all school-admin FTE in both columns.

| District | All reporting schools | P-coded schools | FTE / all reporting schools | Same total FTE / P-coded school |
| --- | --- | --- | --- | --- |
| Riverview | 7 | 5 | 1.65 | 2.31 |
| Snoqualmie Valley | 13 | 11 | 1.97 | 2.33 |
| Northshore | 36 | 32 | 1.72 | 1.94 |
| Monroe | 12 | 8 | 1.54 | 2.31 |

The earlier conclusion that Riverview has lower school-admin FTE per school than both Snoqualmie Valley and Northshore is conditional on counting all reporting programs. With the P-coded denominator, Riverview is approximately equal to Snoqualmie Valley and above Northshore. Neither denominator allocates administrators to actual campuses; a staffing/location crosswalk is needed to evaluate individual-school provision.

## Riverview latest-year change

Central-admin FTE increased from 2.919 to 4.000 (+37.0%). Compensation per admin FTE changed -3.1%; student FTE changed -4.4%. Nominal compensation per 1,000 student FTE changed +39.0%.

The latest increase reflects more reported central-admin FTE and fewer students. Average compensation per FTE fell. Vacancies, partial-year staffing, duties, and reclassification have not been resolved, so these are accounting drivers rather than established causes.

## Public-facing conclusion

Riverview’s strict central-administration compensation per student exceeds nearby larger districts, primarily reflecting higher reported staffing per student. It is close to the median of selected districts with similar enrollment. Including operational Director/Supervisor roles changes the size-peer comparison. School staffing comparisons depend on how alternative and program schools are counted. The evidence warrants reviewing duties and staffing changes; it does not support a finding of waste or overpayment.

## Evidence still needed

- Documented duty/assignment codes or district position descriptions to allocate directors by function consistently across districts.
- A school/program-to-campus and administrator-location crosswalk, including shared assignments and outsourced services.
- Same-year student needs, service responsibilities, and independent peer personnel reconciliation.
- An explanation of Riverview’s central FTE change from 2023-24 to 2024-25 supported by staffing/position records.

## Provenance and reproduction

Generated from [comparison.json](comparison.json) and [school-administration.json](school-administration.json). [evaluation.json](evaluation.json) records input and evaluator hashes and all scenario values. Run `PYTHONPATH=src python -m rsd407_pay.peer_evaluation`. No raw captures or category assignments are changed.

- Adding every Director/Supervisor is a consistent sensitivity scenario, not an established central-office total or statistical confidence bound.
- The P-only denominator retains the full school-admin FTE numerator; it is not staffing allocated to P schools and is not a physical-campus count.
- The six size peers are drawn from the selected nearby cohort, not all Washington districts; medians are descriptive, not statistical significance tests.
- Source year labels, program mix, services, outsourcing and independent peer reconciliation remain review requirements.
- Same-year CPI adjustment applies the same factor to these districts and does not change their relative ratios. Latest-year growth here is nominal.
