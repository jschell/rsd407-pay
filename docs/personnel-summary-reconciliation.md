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
