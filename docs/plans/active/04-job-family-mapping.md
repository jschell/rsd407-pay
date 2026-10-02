# Plan 04 — Job-family mapping

## Goal

Create a transparent, version-controlled mapping from the OSPI-published S-275 duty vocabulary to broad analytical job families.

## Requirements

- Base mappings on OSPI documentation and the exact observed `Duty Title` vocabulary.
- Preserve original code/title alongside mapped category.
- Support one employee having multiple assignments/categories.
- Define rules for:
  - headcount by category;
  - primary-category headcount if needed;
  - FTE allocation across categories;
  - mixed certificated/classified assignments.
- Maintain an explicit `unmapped` bucket.
- Treat new/unrecognized codes as validation failures or review items.

## Deliverables

- mapping file (CSV/YAML/JSON);
- mapping documentation;
- unit tests covering every observed code;
- coverage report by year.

## Acceptance

100% of material RSD407 FTE is mapped or explicitly classified as unresolved with documented reason.


## Implementation sequence

1. Inventory the observed S-275 headers that identify duty/assignment codes across every schema era.
2. Add the documented code field(s) to the canonical row while preserving the source duty title.
3. Produce a per-year code/title/FTE coverage inventory from the real RSD407 dataset.
4. Build the versioned job-family mapping from OSPI documentation and observed codes.
5. Fail or explicitly flag new/unrecognized material codes; never infer categories from employee names or free-text titles.

The mapping itself must not be implemented until steps 1-3 establish the code field and its longitudinal coverage.


## Source-field discovery result

The reproducible all-final run 36958066362 inspected every personnel sheet from 2013-14 through 2024-25. No public workbook exposes a duty/assignment code column. The relevant longitudinal source field is `Duty Title`; `Location Code` appears from 2022-23 onward but identifies location, not job assignment.

Accordingly, Plan 04 will map the exact OSPI-published `Duty Title` vocabulary rather than fabricate or infer an unavailable code. The 12-year RSD407 normalized dataset contains 27 distinct duty titles across 5,019 employee-year rows. Mapping must be exhaustive over those exact source values and retain the original title.
