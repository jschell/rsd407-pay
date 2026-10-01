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
