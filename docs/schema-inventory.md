# S-275 schema inventory

Plan 03 normalization is based on observed, content-validated OSPI workbooks rather than assumed annual schemas.

## Observed schema families

The all-final collection validated 12 annual personnel workbooks from 2013-14 through 2024-25.

- **legacy-core (2013-14 through 2021-22):** stable core personnel fields including district, duty title, certificated/classified FTE, base salary, total salary, insurance benefits, mandatory benefits, and name/certificate fields.
- **2022-plus (2022-23 through 2024-25):** retains the core fields and adds location code, building location name, sex, Hispanic indicator, race, highest degree, and certificated years of experience.

The 2013-14 and 2014-15 validated header rows contain duplicate `cert #` labels. Normalization must therefore preserve columns by position before assigning canonical names; it must not first convert a row to a dictionary keyed only by source header text.

## Reproducible inventory

After an all-final collection:

```bash
PYTHONPATH=src python -m rsd407_pay.schema
```

This reads the collection manifest's validated workbook identities and writes `artifacts/schema-inventory.json`. Each annual entry records the source hash, workbook format, matched sheet, ordered headers, duplicate-header counts, and schema family.

The inventory is an input to adapter design. It is not itself the canonical longitudinal dataset.
