# Canonical S-275 row schema

Plan 03 normalizes source rows without assigning analytical job families. Job-family classification remains Plan 04.

The adapter preserves source provenance on every row:

- `school_year`
- `source_sha256`
- `source_sheet`
- `source_row`

Initial canonical personnel fields are:

- district name
- employee name
- duty title
- certificated FTE
- classified FTE
- base salary
- total salary
- insurance benefits
- mandatory benefits
- last name
- first name
- certificate number
- location code and location name when present

Source headers are indexed by position. Duplicate source labels therefore remain addressable rather than being silently overwritten. Known aliases such as `Clas FTE` / `Class FTE` are explicit.

RSD407 selection currently requires the normalized source district name to equal `Riverview School District`. It does not use employee names, duty titles, or fuzzy matching. A documented district code can be added when confirmed consistently in the source schema.

This adapter layer intentionally does not yet allocate employee-level compensation across assignments. That belongs with the aggregation rules after source row grain is characterized.
