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

Complete with explicit coverage and source-semantic limitations. The completion evidence below records passing checks and accepted limitations.

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

### Implemented architecture sequence (historical decision)

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


## Evidence review after PR 89

The complete retained-source analysis passed in run 37406368550, and merged-main unit CI passed in run 37406671860. See [the aggregate evidence review](../../plan07-evidence-review.md) for twelve-year Access-to-extract comparisons, annual warning counts/amounts, exact annual-change decompositions, and independent-control limitations.

The next PR adds a permanent twelve-year Access-to-extract gate and separately corroborates warning diagnostics directly from SHA-verified retained Access databases in PR CI. Both the source-warning job and complete integration run passed in run 37408082579. Total salary/benefit presentation differences and individual payroll causes remain explicitly unresolved; do not describe them as independently validated.

## Completion evidence and accepted limitations

- [Run 37408082579](https://github.com/jschell/rsd407-pay/actions/runs/37408082579), implementation commit `7b9826b2e9347a481ad6ca19529530b4cf520456`: all 67 unit tests, complete retained analysis (including findings), permanent Access-to-extract gate, and direct Access-source warning corroboration passed.
- All twelve years, 2013-14 through 2024-25, pass internal checks. Registered Access headcount and monetary totals match exactly; FTE differs only within the existing 0.000001 allowance. Access is explicitly a same-system check.
- The 293 zero-FTE and 303 salary-below-base employee-year conditions and their associated amounts match the SHA-verified Access databases in every year. Preserve them as source conditions; individual payroll causes remain unknown.
- Independent Table 45B FTE and base salary pass for 2019-20 through 2024-25 within mathematical display rounding. Earlier annual independent reports are unavailable and documented.
- Published total salary/insurance/mandatory-benefit semantics remain unresolved. Material differences are preserved in the evidence review; no independent validation claim is made for these measures.
- Large annual movements are decomposed into recorded categories/components; causal explanations are not established.
- Source URLs/hashes and aggregate evidence are committed. Source files remain immutable. PR 75 is closed as superseded by merged PR 88.

See [the reproducible review](../../plan07-evidence-review.md), [aggregate comparisons](../../evidence/plan07-review.json), and [source-warning verification](../../evidence/plan07-source-warnings.json). Plan 08 reporting must carry these limitations forward. Completion validates the defined extract pipeline, not payroll correctness or unrestricted comparability with every published measure.
