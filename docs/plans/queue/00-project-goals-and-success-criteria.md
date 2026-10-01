# Plan 00 — Project goals and success criteria

## Goal

Create a durable, reproducible record of RSD407 staffing and compensation trends using public data, beginning with final OSPI S-275 school years 2013-14 through 2024-25.

## Objectives

1. Produce a canonical longitudinal dataset for RSD407.
2. Preserve enough source detail that an independent reviewer can reproduce every published aggregate.
3. Define broad employee categories consistently across years despite source schema changes.
4. Compare staffing using both unique people and FTE.
5. Measure compensation using clearly separated components.
6. Normalize trends for enrollment and inflation where appropriate.
7. Make collection and transformation executable in GitHub Actions.
8. Publish machine-readable outputs plus human-readable summaries.

## Core analytical outputs

For every final school year and broad category:

- unique employees;
- certificated FTE;
- classified FTE;
- total FTE;
- base salary;
- total salary;
- supplemental salary where available;
- insurance benefits;
- mandatory benefits;
- total employer compensation where derivable;
- category share of district staffing/payroll;
- employees and FTE per 1,000 students where enrollment is available;
- nominal and inflation-adjusted compensation measures.

## Initial broad categories

- teachers;
- other certificated instructional staff;
- principals / assistant principals;
- central administration;
- paraeducators / instructional aides;
- clerical / office;
- transportation;
- food service;
- custodial / maintenance / facilities;
- technical / professional support;
- other classified;
- uncategorized / mapping-review.

## Success criteria

- All 2013-14 through 2024-25 final years are collected or explicitly documented as unavailable.
- Every source file has provenance metadata and a cryptographic hash.
- RSD407 rows can be regenerated from raw public source files without manual editing.
- Category mappings are versioned and tested.
- Annual district totals reconcile to authoritative OSPI summaries within documented tolerances.
- A single workflow can rebuild analytical outputs from source inputs.
- Results clearly distinguish final from preliminary data.
- Any unmapped or structurally changed source records fail validation or are surfaced for review.
