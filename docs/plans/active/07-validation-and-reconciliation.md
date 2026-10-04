# Plan 07 — Validation and reconciliation

## Goal

Ensure the longitudinal dataset is trustworthy before interpretation.

## Checks

- district identity/code validation;
- expected year coverage;
- source hash/type validation;
- schema completeness;
- duplicate detection;
- impossible/negative FTE or pay;
- unmapped duty codes;
- annual employee/FTE totals;
- compensation totals;
- reconciliation against OSPI personnel summary reports or other authoritative aggregates;
- large unexplained year-over-year discontinuities;
- parser regression tests.

## Deliverables

- machine-readable validation report;
- human-readable reconciliation table;
- CI gate that blocks reporting when critical checks fail.

## Acceptance

Every annual dataset either passes validation or is visibly excluded with a documented reason.

## Status

Active. First implementation establishes the machine-readable internal validation gate. Independent OSPI aggregate reconciliation remains required before completion.

## Independent control source

Use OSPI final Personnel Summary Reports as the independent published control family. See `docs/personnel-summary-reconciliation.md`. Reconciliation must account for the documented semantic difference between OSPI's full reporting database and the simplified public S-275 extract rather than requiring blind equality.
