# Plan 03 — S-275 schema normalization

## Goal

Normalize annual S-275 files into one stable longitudinal schema despite year-to-year column/name changes.

## Canonical grain

Retain enough detail to represent employee assignments without losing the ability to compute unique employees.

Suggested normalized fields:

- school_year;
- district_code;
- district_name;
- employee/person identifier available in source;
- assignment/duty code;
- duty title;
- location/school;
- certificated_fte;
- classified_fte;
- base_salary;
- total_salary;
- supplemental compensation fields when available;
- insurance_benefits;
- mandatory_benefits;
- program/funding fields useful for validation;
- source row identifier;
- source file hash.

## Work

- Write per-era adapters rather than burying schema drift in one parser.
- Normalize numeric/null formats.
- Detect duplicate source records.
- Document any years where identifiers or compensation fields materially differ.
- Produce Parquet as the canonical normalized analytical input.

## Acceptance

All final years can be parsed into the same canonical schema and validated without manual spreadsheet edits.


## Completion evidence

Completed against the real all-final collection in GitHub Actions run 36942390722.

- 12/12 final school years from 2013-14 through 2024-25 collected, workbook-validated, hash-verified, parsed, and normalized without manual spreadsheet edits.
- RSD407 canonical output contains one row per employee in every year; annual row counts equal annual unique employee-name counts.
- Row-level source provenance is retained (school year, source SHA-256, sheet, and source row).
- Annual FTE, salary, and benefit controls were reviewed for structural discontinuities before closure.
- Known source/schema characteristics are preserved for downstream handling: certificate number is absent from 2022-23 onward; zero-FTE employees and rows where total salary is below base salary are retained rather than silently rewritten.
- The 2018-19 base-salary control total rises materially relative to 2017-18 and should be investigated in longitudinal interpretation, but no normalization/schema break was observed.

Plan 04 owns duty/title-to-job-family classification. Plan 05 owns employee/category aggregation and compensation semantics.
