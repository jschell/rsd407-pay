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
