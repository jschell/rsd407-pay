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

- Personnel Summary inventory run 37238268709 retained and inventoried six final reports (2019–20 through 2024–25). Table 45B is the leading all-program district FTE control; 2024–25 independently reports 337.36 FTE versus 337.367 derived. Table 14 and Table 37C are retained as count/compensation candidates pending definition checks across years.


## Reconciliation architecture decision — structured source + versioned controls

Repeated runtime parsing of Personnel Summary PDFs is removed from the normal analysis design.

OSPI publishes final S-275 Microsoft Access databases for every project year, 2013–14 through 2024–25. These databases are the authoritative structured S-275 source and will be used to derive reproducible district-level control measures without PDF layout parsing. Because they are derived from the same S-275 reporting system, they are a structured-source cross-check, not an independent external validation source.

The repository will also version a small, reviewable control dataset containing the accepted Riverview district controls. Each record must include:

- school year and district code;
- control measure and value;
- source class (`s275_access` or `personnel_summary_published`);
- official source URL;
- immutable source SHA-256;
- source table/query or published report table;
- PDF page and literal published source row when the source is a Personnel Summary report;
- extraction/parser version;
- derivation method;
- review status.

Normal retained analysis consumes this versioned control dataset and does not invoke `pdftotext`.

Personnel Summary reports remain the independent published control family where annual reports are available. The already validated Table 45B FTE reconciliation remains an external check. Published compensation rows will be retained in the control dataset rather than reparsed on every analysis run.

### Implementation sequence

1. Freeze PR 75; do not merge its pre-architecture runtime PDF compensation gate.
2. Add a source registry for the twelve official final S-275 Access databases.
3. Add an ingestion utility that downloads/hashes the Access source and inventories its tables/queries before any compensation derivation is assumed.
4. Establish explicit, versioned derivations for district all-program FTE and compensation from the Access schema.
5. Create and commit the provenance-rich control dataset.
6. Populate published Personnel Summary controls from reviewed evidence, retaining literal source rows/pages and source hashes.
7. Add a regeneration/verification command that compares newly derived structured controls with the committed dataset and fails on unexplained drift.
8. Change retained analysis to consume the committed controls; PDF extraction is verification/regeneration tooling only.
9. Reconcile the structured S-275 derivation, simplified public extract, and independent published Personnel Summary controls. Only definitionally equivalent measures become validation gates.
10. Supersede or rebuild PR 75 on this architecture after the complete control set passes verification.

### Acceptance additions

- No production analysis step depends on PDF text layout.
- Every committed control is traceable to a SHA-identified official OSPI source.
- All twelve project years have an official structured S-275 source registered or are visibly excluded with a documented reason.
- Regeneration of committed controls is deterministic and separately testable.
- Personnel Summary controls retain their independent-source identity and are never conflated with Access-derived S-275 controls.
