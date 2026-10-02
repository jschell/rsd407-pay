# Plan 04 — Job-family mapping

## Goal

Create a transparent, version-controlled mapping from the OSPI-published S-275 `Duty Title` vocabulary to broad analytical job families without inventing assignment detail that is absent from the public source.

## Established source semantics

Real-workbook inspection across every final year from 2013-14 through 2024-25 established that the public personnel sheets expose no duty/assignment code. The longitudinal classification key is the exact OSPI-published `Duty Title`.

The normalized source grain is one employee row per school year, not assignment-level rows. A row can contain certificated and classified FTE, but hidden assignments cannot be reconstructed or allocated among job families.

## Implementation

- Preserve the original `duty_title` on every canonical/enriched row.
- Map exact title values only; no employee-name, substring, or fuzzy inference.
- Maintain the versioned mapping in `config/job-family-mapping.json`.
- Fail analysis when a newly observed title is not explicitly mapped.
- Produce annual job-family row and FTE coverage.
- Reconcile enriched row/FTE totals to the canonical input.
- Use conservative broad categories when the public source lacks assignment context.

## Acceptance evidence

Canonical retained source: `s275-source-2026-10-02`.

Successful snapshot-analysis run: `37024261598` at commit `bbec320c8afe139dd006955e8ddac5affa583f14`.

The validated 2013-14 through 2024-25 series contains:

- 5,019 employee-year rows;
- 27 exact OSPI-published duty titles;
- zero unknown duty titles after applying the versioned mapping.

The successful run downloaded the retained release snapshot, verified source hashes, normalized the series, generated source-field and exact-title coverage, applied the job-family mapping, and uploaded the derived analysis artifact.

`Director/Supervisor`, `Operator`, and `Service Worker` remain conservatively in `other classified` because the employee-level public source lacks the assignment/activity context needed to divide them reproducibly among transportation, food service, facilities, technical, or related functions.

## Acceptance

Complete. All observed titles in the canonical snapshot are explicitly mapped, future unknown titles fail validation, original source titles are retained, and row/FTE reconciliation is tested. Results must be described as employee-year duty-title families rather than assignment-level allocation.
