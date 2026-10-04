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

## Enrollment control: Table 47

The primary district-grain reconciliation target is OSPI Personnel Summary **Table 47 — Selected Personnel Data by School District**. It exposes district-level student enrollment/FTE and personnel FTE/salary measures.

Comparison status is field-specific:

- student FTE: comparable when the report confirms the same annual-average enrollment basis;
- certificated FTE: candidate pending scope confirmation;
- classified FTE: candidate pending scope confirmation;
- average salary: candidate only; do not equate it with this project's aggregate salary/FTE without confirming OSPI's numerator and personnel scope.

The implementation records these semantics in the machine-readable Table 47 control inventory before extracting numeric controls.

## Table 47 confirmed scope

Retained final reports confirm Table 47 is **School Districts Ranked by FTE Enrollment (Report P-223)**. It is therefore an independent rounded enrollment control, not a personnel FTE or salary control. For Riverview (district 17407), the retained reports publish 3,224 (2019-20), 2,928 (2020-21), 2,942 (2021-22), 2,985 (2022-23), 2,949 (2023-24), and 2,819 (2024-25). Reconciliation compares these values with the project's P-223 annual-average student FTE after whole-student rounding. Personnel FTE and compensation require separate Personnel Summary tables with matching definitions.

## Personnel-control discovery

Table 47 is reserved for P-223 enrollment reconciliation. Personnel FTE and compensation controls must be selected from the retained report's personnel-specific district tables only after their published definitions are matched to the simplified public S-275 extract. The repository inventories table titles from every retained annual report before selecting a control; it does not infer equivalence from similar field names.

## Confirmed personnel control candidates

The retained 2019–20 through 2024–25 final reports have a stable personnel-table structure. Direct inspection identifies these controls for definition testing:

- **Table 45B — Comparison of Certificated and Classified FTE Staff in All Programs with FTE Students.** This is the primary independent FTE candidate because it reports district-level certificated instructional, certificated administrative, and classified FTE across all programs. For 2024–25, Riverview reports 196.19 + 15.26 + 125.91 = 337.36 FTE, compared with 337.367 from the normalized public S-275 extract. This near-exact agreement supports population equivalence, subject to validation across every retained year.
- **Table 14 — Unduplicated Individual and FTE Counts.** This is a candidate control for employee counts and certificated/classified composition, but its mixed-personnel columns must be interpreted before comparison with the simplified one-major-assignment public extract.
- **Tables 34B and 36B — Certificated Instructional/Administrative Staff in All Programs.** These provide the certificated compensation components in 2019–20 through 2022–23.
- **Table 37C — Certificated Staff in All Programs.** This consolidated certificated control is available in 2023–24 onward.
- **Table 38B — Classified Staff in All Programs.** This is the classified compensation control across all six retained reports.

Compensation reconciliation combines the certificated and classified all-program controls without allocating employee-level public-extract salary to certificated/classified FTE. The comparison derives a display-rounding bound from published FTE precision (hundredths) and published average-per-FTE precision (whole dollars). It remains evidence rather than a hard validation gate until the retained six-year comparison is reviewed.

Table 45 (without B) is basic-education-only and is not equivalent to the project's all-program S-275 population. Table 47 remains an enrollment-only P-223 control.
