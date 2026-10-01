# Source provenance

The authoritative source registry is `config/sources.json`. Source discovery is restricted to OSPI hosts and expected final school years.

For each collected file, provenance records must include school year, source page, direct URL, format, retrieval timestamp, SHA-256, byte size, HTTP status/content type, and parser/schema version.

A discovery check is intentionally different from a full download. Pull requests run discovery so link drift is detected cheaply. Plan 02 will add full collection/download workflows and immutable raw-file handling.

Third-party payroll sites are not permitted as silent substitutes for missing OSPI files.
