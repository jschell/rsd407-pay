# Plan 05 — Aggregation and compensation metrics

## Goal

Generate consistent annual RSD407 staffing and compensation metrics.

## Metrics

By school year and broad category:

- unique employee count;
- assignment count;
- certificated, classified, and total FTE;
- base salary totals;
- total salary totals;
- supplemental salary totals where available;
- insurance and mandatory benefit totals;
- total employer compensation where supported;
- salary/compensation per FTE;
- median employee compensation where source grain supports it;
- category share of district total;
- year-over-year and baseline change.

## Guardrails

- Never treat headcount and FTE as interchangeable.
- Never average salaries across partial-year/part-time people without labeling the denominator.
- Prefer per-FTE compensation for category comparison.
- Keep salary and employer-paid benefits separate in source tables even when also providing a combined metric.

## Acceptance

Generated aggregates are deterministic and traceable back to normalized source rows.
