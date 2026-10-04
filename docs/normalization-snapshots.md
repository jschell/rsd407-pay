# Normalization source snapshots

Plan 06 normalization inputs are retained independently from the S-275 personnel snapshot.

The publisher collects the two bounded BLS CPI API responses and the OSPI P-223 final enrollment workbook once, derives the accepted CPI and Riverview enrollment outputs from those same inputs, hashes raw and derived files, verifies the manifest, and publishes the complete `artifacts/normalization` tree as an immutable GitHub Release archive.

Release tags are write-once by workflow policy. If an upstream source changes, publish a new tag rather than replacing an existing release.

The snapshot contains the exact raw P-223 workbook, both exact BLS response payloads, `cpi.json`, `enrollment.json`, `p223-inventory.json`, and `normalization-source-manifest.json`.

Retained normalization snapshots allow later S-275 analysis to reproduce per-student and constant-dollar metrics without live OSPI or BLS requests.
