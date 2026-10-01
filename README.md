# RSD407 Pay

Reproducible analysis of Riverview School District 407 staffing and compensation using Washington OSPI S-275 personnel data and related public datasets.

## Primary questions

- How has RSD407 staffing changed from 2013-14 forward?
- How many employees and FTEs are in each broad job family?
- How have salaries, supplemental pay, benefits, and total compensation changed?
- How have instructional, school-administration, central-administration, and classified staffing changed relative to enrollment?
- Which changes are nominal versus inflation-adjusted?
- Can every published result be reproduced from cited public source files?

## Project principles

1. Prefer authoritative public sources, especially OSPI S-275.
2. Preserve provenance for every downloaded source.
3. Keep raw source files immutable.
4. Derive categories from documented duty/assignment codes, not employee names.
5. Distinguish unique employees, assignments, and FTE.
6. Distinguish base salary, total salary, benefits, and total employer compensation.
7. Keep preliminary school years separate from final historical series.
8. Make analyses reproducible in GitHub Actions.

## Planned analytical range

Initial historical baseline: **2013-14 through 2024-25 final S-275 data**. Later years can be appended after OSPI marks them final.

See `docs/plans/queue/` for implementation plans.
