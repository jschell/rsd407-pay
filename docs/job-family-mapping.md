# Job-family mapping source field

The public S-275 workbooks were inspected across every final year from 2013-14 through 2024-25.

No public personnel sheet exposes a duty or assignment code. The longitudinal classification field is the OSPI-published `Duty Title`. `Location Code` appears in the 2022-plus schema family and identifies location, not job assignment.

Therefore job-family mapping uses **exact observed Duty Title values** as its authoritative source key. It does not infer categories from employee names, substrings, or fuzzy title matching.

The canonical row preserves the original `duty_title`; `job_family` is a derived analytical field. New titles must be explicitly reviewed rather than silently assigned.

## Source grain limitation

The normalized RSD407 source contains one employee row per school year. It does not expose assignment-level rows. A row can contain certificated and classified FTE fields, but the public source does not provide enough information to allocate an employee among multiple hidden assignments or job families.

Consequently, category results describe the employee-year's OSPI-published duty-title family. They must not be described as assignment-level allocation.

## Coverage

The validated 2013-14 through 2024-25 series contains 5,019 employee-year rows and 27 distinct published duty titles. The snapshot analysis workflow emits exact title, employee-row count, certificated FTE, classified FTE, and total FTE so mapping coverage can be independently checked.

## Mapping policy

The versioned mapping is `config/job-family-mapping.json`. Matching is exact. Any newly observed title fails snapshot analysis and requires an explicit mapping decision.

Broad categories are intentionally limited by the information in the public employee-row workbook. In particular, `Service Worker`, `Operator`, and `Director/Supervisor` are retained as `other classified` because OSPI's definitions and summary reports require assignment/activity context to distinguish food service, bus operation, maintenance, transportation, data processing, and related functions. That assignment context is not present in this source. The analysis must not manufacture those subcategories from employee names or assumptions.

The mapping therefore favors reproducible coarser categories over falsely precise ones. Original `duty_title` remains in every enriched row.
