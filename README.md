# RSD407 Pay

Reproducible analysis of Riverview School District 407 staffing and compensation using Washington OSPI S-275 personnel data and related public datasets.

## Read the analysis

Start with the [generated staffing and compensation report](docs/reporting/report.md). It includes annual totals, category changes, enrollment-adjusted staffing, both inflation series, and strict central-administration staffing per 1,000 students. [Downloadable tables and input provenance](docs/reporting/) accompany the report.

The analysis distinguishes changes in staffing, enrollment, and compensation. It provides evidence for questions about district spending; it does not establish efficiency, individual payroll correctness, or total operating costs. [Plan 07's evidence review](docs/plan07-evidence-review.md) documents independent-control coverage and unresolved published salary/benefit comparisons.

## Nearby district comparison

The 2024–25 comparison shows Riverview’s strict central-administration compensation per student FTE is **23% above Snoqualmie Valley and 37% above Northshore**. Its school-administrator FTE per reporting school is lower than both. These measures describe staffing and compensation; they do not establish efficiency or whether staffing is necessary.

| District | Student FTE | Reporting schools | Central compensation / 1,000 student FTE | Central FTE / 1,000 student FTE | School-admin FTE / reporting school |
| --- | --- | --- | --- | --- | --- |
| Riverview | 2,818.78 | 7 | $404,596 | 1.42 | 1.65 |
| Snoqualmie Valley | 6,801.25 | 13 | $328,884 | 1.18 | 1.97 |
| Northshore | 21,571.74 | 36 | $294,872 | 0.99 | 1.72 |
| Monroe | 5,437.42 | 12 | $256,020 | 0.92 | 1.54 |
| Lakewood | 2,564.66 | 5 | $890,490 | 3.44 | 1.40 |
| Sultan | 2,038.60 | 8 | $522,040 | 1.93 | 1.00 |
| Granite Falls | 2,163.95 | 6 | $378,351 | 1.39 | 1.17 |
| Tukwila | 2,643.09 | 5 | $437,932 | 1.89 | 1.60 |
| Orting | 2,741.87 | 4 | $400,968 | 1.46 | 2.25 |
| Steilacoom Historical | 2,775.08 | 6 | $287,790 | 1.08 | 1.83 |

Student FTE shows each district’s annual-average K–12 enrollment, including ALE, using the same 2024–25 OSPI P-223 measure as the per-student calculations. Reporting-school counts show the number of school codes with positive enrollment in that year.

Compensation includes reported salary, employer insurance, and mandatory benefits. Strict central administration includes superintendents, deputy/assistant superintendents, and Other District Admin.; **Director/Supervisor roles are excluded** because the source titles span operational functions. School administration includes principals, vice principals, and Other School Admin. Reporting-school counts include alternative/online/program schools with positive enrollment; they are **not physical-campus counts**. Peer totals have not been independently reconciled against published Personnel Summary or Access controls.

- [Central-office comparison and limitations](docs/comparisons/comparison.md)
- [School-administrator FTE per school and school-count definitions](docs/comparisons/school-administration.md)
- [Three-year comparison data: 2013–14, 2023–24, and 2024–25](docs/comparisons/comparison.csv)
- [Source evidence, school lists, and reproduction instructions](docs/comparisons/README.md)

This overview is derived from the committed [staffing comparison JSON](docs/comparisons/comparison.json) and [school-administration JSON](docs/comparisons/school-administration.json). Nearby districts and size peers are shown individually.

## Primary questions

- How has RSD407 staffing changed from 2013-14 forward?
- How many employees and FTEs are in each broad job family?
- How have salaries, supplemental pay, benefits, and total compensation changed?
- How have instructional, school-administration, central-administration, and classified staffing changed relative to enrollment?
- How does central-office and school-administration staffing compare with nearby districts and districts of similar size?
- Which changes are nominal versus inflation-adjusted?
- Can every published result be reproduced from cited public source files?

## Project principles

1. Prefer authoritative public sources, especially OSPI S-275.
2. Preserve provenance for every downloaded source.
3. Keep raw source files immutable.
4. Derive categories from documented duty/assignment codes, not employee names.
5. Distinguish unique employees, assignments, and FTE.
6. Distinguish base salary, total salary, benefits, and total employer compensation.
7. Keep preliminary school years separate from final historical series.
8. Make analyses reproducible in GitHub Actions.

## Planned analytical range

Initial historical baseline: **2013-14 through 2024-25 final S-275 data**. Later years can be appended after OSPI marks them final.

See `docs/plans/queue/` for implementation plans.
