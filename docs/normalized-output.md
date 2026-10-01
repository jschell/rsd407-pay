# Normalized RSD407 output

After collecting all final S-275 years, run:

```bash
PYTHONPATH=src python -m rsd407_pay.pipeline
```

The pipeline verifies every raw file against the SHA-256 recorded in the collection manifest, locates personnel headers in each XLS/XLSX sheet, applies the canonical row adapter, and retains rows whose normalized district name exactly equals `Riverview School District`.

Outputs:

- `artifacts/normalized/rsd407.csv` — canonical source rows with row-level provenance.
- `artifacts/normalized/rsd407-summary.json` — annual row count plus certificated/classified FTE and base/total salary control totals.

The pipeline fails if any collected school year produces no RSD407 rows. The summary is a validation/control artifact, not the final analytical report. Employee headcount, assignment handling, job-family mapping, and compensation allocation are intentionally deferred to Plans 04 and 05.
