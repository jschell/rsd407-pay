# Plan 01 — Source discovery and provenance

## Goal

Build a machine-readable registry of authoritative OSPI S-275 sources for every school year from 2013-14 forward.

## Work

- Identify the canonical OSPI SAFS/S-275 landing page and annual downloadable files.
- Prefer machine-readable Excel/Access sources; allow PDF only as a documented fallback.
- Record for each year:
  - school year;
  - release status (final/preliminary);
  - source page URL;
  - direct download URL;
  - file format;
  - retrieval timestamp;
  - HTTP metadata where useful;
  - SHA-256 hash;
  - byte size;
  - parser/schema version.
- Detect broken redirects, HTML error pages saved as spreadsheets, partial downloads, and anti-bot responses.
- Add retry/backoff and explicit user-agent handling where appropriate.
- Never silently substitute a third-party payroll source for OSPI.

## Deliverables

- `config/sources.yml` or equivalent registry.
- provenance schema.
- collector utility.
- tests using representative fixtures.
- GitHub Actions workflow capable of source discovery/checking.

## Acceptance

The workflow can report the status of all expected annual S-275 sources and fails clearly when an expected source cannot be validated.
