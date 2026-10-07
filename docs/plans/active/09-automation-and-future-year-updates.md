# Plan 09 — Automation and future-year updates

## Goal

Make the project easy to update when OSPI publishes a new final school year.

## Work

- Check for newly published/finalized S-275 sources.
- Preserve historical raw captures and flag URL or hash revisions.
- Require validation before appending a new year to published results.
- Record source revisions and their analytical impact.
- Provide one documented workflow to rebuild all derived outputs.

## Status

Active. The first step adds a final-workbook candidate monitor to the existing weekly/manual source-check workflow. It records source-page URL, capture time, page hash, original HTML, official link evidence, accepted coverage, and candidates outside that coverage. Preliminary/draft links are excluded. Discovery never changes accepted years, downloads/promotes a candidate workbook, or changes published results.

## Historical-source revision monitoring

The next implementation compares current registered-year workbook downloads with the collection manifest from the explicitly accepted immutable snapshot tag. It distinguishes unchanged bytes, URL relocation, content revision, combined revision, and failed observations. Every year is attempted after a per-year error. Changed workbook bytes are retained under year/SHA-256 paths without overwriting accepted sources or existing evidence; workbook identity is checked before capture.

Revision candidates or incomplete checks fail the monitoring command and require review. Reports retain old/new URLs and hashes, observed HTTP/identity metadata, capture time, accepted manifest hashes, and the accepted snapshot tag. Analytical effects remain unassessed until a deliberate rebuild. Monitoring does not replace the accepted release or report.

## Remaining implementation

1. Complete durable revision retention and quantify analytical effects through a reviewed before/after rebuild. The initial byte/URL comparison and changed-byte capture are implemented; temporary workflow artifacts are not permanent revision publication.
2. Replace scattered fixed-year lists and fixed report endpoints with a shared accepted-period contract. Update enrollment, CPI, Access controls, published controls, and all coverage gates together; reject partial updates.
3. Validate new-year workbook identity, schema, categories, normalization sources, same-system controls, and available independent published controls before promotion.
4. Define a reviewed snapshot/control update with reproducible before/after reporting and a durable revision record.
5. Test historical revisions, preliminary-to-final transitions, missing controls, missing normalization years, duplicate years, and reporting endpoints on actual available sources.

## Rebuild current accepted analysis

Run **Analyze retained sources** (`analyze-snapshot.yml`) with explicit immutable S-275 and normalization snapshot tags. It verifies sources, rebuilds normalization, derives and validates all analytical outputs, and generates the report in one workflow. Exact commands and boundaries are in [the update guide](../../future-year-updates.md).

## Acceptance

Adding a newly finalized year is an auditable data update. Existing historical captures remain intact; new sources cannot bypass validation or quietly change report coverage.

The initial final-link monitor is an informational discovery step. It does not complete historical revision detection or future-year ingestion.
