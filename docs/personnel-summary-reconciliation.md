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

## Current implementation

Normal analysis uses committed reviewed controls; source collection and PDF parsing are separate regeneration tools. See [Plan 07 evidence review](plan07-evidence-review.md) for current comparisons and limitations.

## Historical-source status

Current-page discovery covers 2019-20 onward. The six earlier required years (2013-14 through 2018-19) are tracked explicitly in `config/personnel-summary-history.json` and remain unresolved until an official OSPI resource or documented archival source is verified. URL patterns must not be inferred from newer filenames.

## Control tiers

OSPI's current final Personnel Summary Reports include longitudinal tables that reach back across the project's historical period. These are valid independent controls for historical trend measures when definitions match, but they are not substitutes for unavailable year-specific district reports.

Reconciliation therefore uses two explicit tiers:

- **District annual controls:** year-specific final Personnel Summary Reports, where an official annual resource is available.
- **Longitudinal controls:** historical series embedded in a later official OSPI final report, used only for measures whose table definitions match the project output.

The source type must be recorded with every comparison. A later longitudinal table must never be represented as though it were the original annual report for that year.

## Table 47 confirmed scope

Retained final reports confirm Table 47 is **School Districts Ranked by FTE Enrollment (Report P-223)**. It is therefore an independent rounded enrollment control, not a personnel FTE or salary control. For Riverview (district 17407), the retained reports publish 3,224 (2019-20), 2,928 (2020-21), 2,942 (2021-22), 2,985 (2022-23), 2,949 (2023-24), and 2,819 (2024-25). Reconciliation compares these values with the project's P-223 annual-average student FTE after whole-student rounding. Personnel FTE and compensation require separate Personnel Summary tables with matching definitions.

## Personnel-control discovery

Table 47 is reserved for P-223 enrollment reconciliation. Personnel FTE and compensation controls must be selected from the retained report's personnel-specific district tables only after their published definitions are matched to the simplified public S-275 extract. The repository inventories table titles from every retained annual report before selecting a control; it does not infer equivalence from similar field names.

## Confirmed personnel control candidates

The retained 2019–20 through 2024–25 final reports have a stable personnel-table structure. Direct inspection identifies these controls for definition testing:

- **Table 45B — Comparison of Certificated and Classified FTE Staff in All Programs with FTE Students.** This is the primary independent FTE candidate because it reports district-level certificated instructional, certificated administrative, and classified FTE across all programs. For 2024–25, Riverview reports 196.19 + 15.26 + 125.91 = 337.36 FTE, compared with 337.367 from the normalized public S-275 extract. This near-exact agreement supports population equivalence, subject to validation across every retained year.
- **Table 14 — Unduplicated Individual and FTE Counts.** This is a candidate control for employee counts and certificated/classified composition, but its mixed-personnel columns must be interpreted before comparison with the simplified one-major-assignment public extract.
- **Table 37C — Certificated Staff in All Programs.** This is a candidate certificated compensation control. It must not be combined with classified compensation until the corresponding all-program classified table and salary definitions are confirmed.

Table 45 (without B) is basic-education-only and is not equivalent to the project's all-program S-275 population. Table 47 remains an enrollment-only P-223 control.


## Committed published controls

Normal retained analysis consumes `controls/personnel-summary-published.json`; it does not download or parse Personnel Summary PDFs. The committed records retain the official URL, immutable SHA-256, published table/page, literal compensation row, and review status. PDF parsing remains regeneration/evidence tooling.

For 2019–20 through 2024–25, Table 45B remains the independent all-program FTE gate. Published compensation provides a second independent gate: district base salary reconstructed from the definitionally equivalent all-program certificated/classified rows must fall within the exact display-rounding bound implied by hundredth-rounded FTE and whole-dollar average salary/FTE.

Total salary, insurance benefits, and mandatory benefits are retained as semantic-review evidence because their published definitions do not reconcile within display rounding in every year. No arbitrary percentage tolerance is used to force agreement. Annual Personnel Summary coverage before 2019–20 remains explicitly unavailable.

