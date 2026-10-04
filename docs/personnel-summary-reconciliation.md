# OSPI personnel-summary reconciliation source

Plan 07 uses OSPI's final annual **Personnel Summary Reports** as the independent published control family for the normalized public S-275 extract.

Official source page: https://ospi.k12.wa.us/policy-funding/school-apportionment/school-publications/personnel-summary-reports

## Why this is independent enough to be useful

OSPI describes these reports as annual summaries of certificated and classified personnel data, including salaries and benefits. The reports are produced from district S-275 submissions and published separately from the simplified public personnel spreadsheets used by this project.

OSPI's documented reporting workflow also distinguishes the full Access database/reporting process from the simplified public files. The simplified public version uses one major assignment record per personnel record and a subset of the full S-275 fields. Therefore reconciliation is expected to identify both matches and semantic differences; it must not assume every official summary measure can be reconstructed exactly from the simplified extract.

## Reconciliation strategy

For every school year 2013-14 through 2024-25:

1. discover the final Personnel Summary Report from the official OSPI page;
2. retain the report URL, retrieval timestamp, and SHA-256 of the downloaded source;
3. extract Riverview using district code 17407, not fuzzy district-name matching;
4. inventory the district-level control measures available in that year's report before choosing comparisons;
5. compare only measures with equivalent definitions to the project outputs;
6. record absolute and percentage differences and a status for every comparison;
7. classify non-equivalent measures as not-comparable with a documented reason rather than forcing a pass/fail;
8. treat unexplained material differences as validation failures or visible exclusions.

The 2024-25 final report independently shows Riverview (17407) at approximately 2,819 annual-average FTE students, consistent with the project's P-223 extraction of 2,818.78. This is a useful cross-source denominator check but is not by itself sufficient personnel reconciliation.

## Next implementation

Build a reproducible collector/inventory for the historical final Personnel Summary Reports. Do not hard-code control totals copied from PDFs. The collector should establish which district-level tables and measures are consistently available across all 12 years before the reconciliation gate is finalized.

## Historical-source status

Current-page discovery covers 2019-20 onward. The six earlier required years (2013-14 through 2018-19) are tracked explicitly in `config/personnel-summary-history.json` and remain unresolved until an official OSPI resource or documented archival source is verified. URL patterns must not be inferred from newer filenames.

## Control tiers

OSPI's current final Personnel Summary Reports include longitudinal tables that reach back across the project's historical period. These are valid independent controls for historical trend measures when definitions match, but they are not substitutes for unavailable year-specific district reports.

Reconciliation therefore uses two explicit tiers:

- **District annual controls:** year-specific final Personnel Summary Reports, where an official annual resource is available.
- **Longitudinal controls:** historical series embedded in a later official OSPI final report, used only for measures whose table definitions match the project output.

The source type must be recorded with every comparison. A later longitudinal table must never be represented as though it were the original annual report for that year.

## Primary district control: Table 47

The primary district-grain reconciliation target is OSPI Personnel Summary **Table 47 — Selected Personnel Data by School District**. It exposes district-level student enrollment/FTE and personnel FTE/salary measures.

Comparison status is field-specific:

- student FTE: comparable when the report confirms the same annual-average enrollment basis;
- certificated FTE: candidate pending scope confirmation;
- classified FTE: candidate pending scope confirmation;
- average salary: candidate only; do not equate it with this project's aggregate salary/FTE without confirming OSPI's numerator and personnel scope.

The implementation records these semantics in the machine-readable Table 47 control inventory before extracting numeric controls.
