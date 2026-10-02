# Plan 04 duty-code discovery

Job-family classification must be based on documented OSPI duty/assignment identifiers, not employee names and not free-text title heuristics.

Before adding a mapping table, inspect the validated S-275 schemas and real RSD407 rows to establish:

- the source header(s) carrying duty/assignment codes in each schema family;
- whether codes are stable across 2013-14 through 2024-25;
- whether one normalized employee row can encode multiple assignments;
- the relationship between code, duty title, certificated FTE, and classified FTE;
- annual code/title/FTE coverage and an explicit unresolved bucket.

Until this discovery is complete, `duty_title` is descriptive source data only and must not be used as the authoritative category key.
