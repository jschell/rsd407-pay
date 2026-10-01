# AGENTS.md

## Purpose

This repository builds a reproducible public-data analysis of Riverview School District 407 staffing and compensation.

## Non-negotiable requirements

- Do not fabricate or hand-enter analytical results when source data can be collected programmatically.
- Preserve source provenance: source URL, school year, retrieval timestamp, file hash, and parser version.
- Treat downloaded raw files as immutable inputs.
- Keep preliminary and final OSPI releases distinct.
- Use documented OSPI identifiers/duty codes for categorization.
- Do not infer employment category from names.
- Separate headcount, assignment count, and FTE.
- Tests must cover schema drift, duplicate handling, category mapping, and aggregate reconciliation.
- Workflows should fail loudly when a source changes unexpectedly rather than silently producing partial results.
- Generated outputs must state source years and any known limitations.

## Plan lifecycle

- `docs/plans/queue/`: approved but not started.
- `docs/plans/active/`: currently executing.
- `docs/plans/complete/`: completed plans with completion notes/evidence.

Move plans between states instead of duplicating them.
