# Plan 09 — Automation and future-year updates

## Goal

Make adding a newly finalized year or reviewing historical source revisions reproducible and auditable.

## Implemented

- Final-source candidate monitoring preserves official link/page evidence and excludes preliminary/draft labels.
- Historical revision monitoring compares every accepted year with an explicitly pinned immutable manifest, preserves changed bytes separately, and continues through individual failures.
- Shared accepted-period coverage drives discovery, enrollment, normalization, validation, and reporting endpoints.
- The retained analysis rejects incomplete source/enrollment/CPI/Access/published-control updates; it rebuilds all outputs and the report from explicit immutable tags.
- Period-aware CPI capture and hash-verified replay handle new window endpoints. Final enrollment discovery requires stated coverage and actual sheet/district validation.
- Revision impact tooling verifies successful report provenance and all input hashes/gates, compares district/category/normalization/administration measures, and bundles before/after evidence.
- A manual review workflow downloads two successful retained analyses and can publish a reviewed record and evidence bundle under a new revision tag only when the supplied reviewed record hash matches. Existing tags are never replaced. Source acceptance/report promotion remain separate reviewed changes.

## Verification

All 87 local tests pass, including revised bytes, fail-complete monitoring, invalid/duplicate periods, missing future-year dependencies, future CPI/enrollment endpoints, duplicate comparison rows, tampered inputs, failed gates, and exclusive evidence creation.

The generated [historical compatibility record](../../revisions/2026-10-07-normalization-refactor.json) compares actual retained-analysis runs 37567682169 and 37569049798. Their validation gates and file hashes pass, with no changes in compared analytical measures. Both reference the same accepted immutable source captures.

## Remaining before completion

1. After merge, execute the new manual revision-review workflow against these known successful runs, review its record hash, and verify publication under a new revision tag. This proves the workflow and durable evidence path, beyond local comparison tests.
2. Verify the documentation and publication safeguards from that run; record the run/release evidence and move this plan to complete only after success.
3. A future real upstream revision/new year still requires new immutable captures, reviewed controls and full before/after analysis. No actual revision is invented to satisfy testing. Future-year tests are synthetic; current retained CI covers the actual available period.

## Limits and acceptance

Independent published controls before 2019-20 remain unavailable. Unresolved published benefit/total-salary semantics and retained source anomalies remain explicit limitations. The 2025 dollar base stays fixed for comparability. Monitoring, evidence publication, and source acceptance are distinct actions.

Follow [the update guide](../../future-year-updates.md) for rebuild, capture, comparison, publication, and report promotion. Acceptance requires existing captures to remain intact and new sources to pass all gates without quietly changing report coverage.
