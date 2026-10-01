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
