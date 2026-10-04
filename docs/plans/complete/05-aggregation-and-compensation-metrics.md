# Plan 05 — Aggregation and compensation metrics

## Goal

Generate deterministic annual RSD407 staffing and compensation metrics from the job-family-enriched employee-year dataset.

## Source semantics

The public S-275 source is one employee row per school year, not assignment-level data. Therefore Plan 05 reports employee-year headcount and FTE; it does not report or infer assignment counts.

Job-family metrics describe the employee-year's exact OSPI Duty Title mapping. They are not assignment-level allocation.

## Core metrics

By school year and broad job family:

- employee-year row/headcount count;
- certificated, classified, and total FTE;
- base salary total;
- total salary total;
- insurance benefit total;
- mandatory benefit total;
- combined reported employer compensation where component support is explicit;
- base salary per FTE and total salary per FTE when total FTE is nonzero;
- category share of district FTE, base payroll, and total payroll;
- year-over-year changes after annual aggregates are established.

District annual totals must also be emitted for reconciliation.

## Guardrails

- Never treat headcount and FTE as interchangeable.
- Do not infer assignment count.
- Preserve zero-FTE employee rows in headcount/payroll totals; do not divide their compensation by zero.
- Salary/FTE is an aggregate ratio (sum salary / sum FTE), not an average of individual salary/FTE values.
- Keep base salary, total salary, insurance benefits, and mandatory benefits as separate source-derived components.
- Do not silently repair rows where total salary is less than base salary; preserve source values and surface data-quality counts.
- Do not manufacture supplemental-pay components when the canonical schema does not expose them consistently.
- All category totals must reconcile to district totals within numeric tolerance.
- Inflation adjustment, enrollment/per-pupil normalization, and interpretive trend analysis are outside this core aggregation step.

## Acceptance

- Aggregates are deterministic and traceable to the enriched canonical rows.
- Annual category row counts, FTE, payroll, and benefits reconcile to annual district totals.
- Zero-FTE and total-salary-below-base conditions are explicitly counted.
- No assignment-level claims are emitted.

## Real-data acceptance evidence

Retained snapshot analysis run 37175051934 on commit 7602509 successfully processed 5,019 employee-year rows across all 12 school years, mapped zero unknown duty titles, emitted 108 year/family groups, and passed runtime category reconciliation.

Observed source-quality conditions are preserved rather than corrected. Zero-FTE row counts range from 11–36 in 2013–14 through 2023–24 and fall to 2 in 2024–25. Rows where reported total salary is below reported base salary range from 12–54 annually and peak at 54 in 2023–24. These counts alone do not establish payroll errors; they identify source rows requiring caution in interpretation.

The snapshot workflow emits `data-quality.json` with annual and job-family breakdowns so these conditions remain independently reviewable.

## Final acceptance

Plan 05 acceptance was confirmed by retained-snapshot run 37175619772 on commit d2345a8. The run processed all 12 school years and 5,019 employee-year rows, mapped zero unknown duty titles, emitted 108 year/family groups, passed runtime category reconciliation, generated the source-quality artifact, and uploaded the normalized analysis artifact.

The quality breakdown shows historical zero-FTE rows are overwhelmingly concentrated in technical/professional support (for example, 30 of 37 rows in that family in 2023–24) and that this pattern disappears in 2024–25. This is retained as a source/reporting-semantic discontinuity and is not repaired or interpreted as a staffing change. Total-salary-below-base conditions occur across multiple families, particularly classified and paraeducator/aide rows, and remain explicit source-quality flags.

Plan 05 is complete. Enrollment denominators, CPI adjustment, constant-dollar measures, and per-pupil metrics proceed separately under Plan 06.
