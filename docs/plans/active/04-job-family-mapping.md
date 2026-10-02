# Plan 04 — Job-family mapping

## Goal

Create a transparent, version-controlled mapping from OSPI duty/assignment codes to broad analytical job families.

## Requirements

- Base mappings on OSPI documentation and observed duty codes.
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
