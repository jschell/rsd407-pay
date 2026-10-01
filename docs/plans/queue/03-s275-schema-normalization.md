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
