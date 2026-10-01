# Plan 01 — Source discovery and provenance

## Goal

Build a machine-readable registry of authoritative OSPI S-275 sources for every school year from 2013-14 forward.

## Work completed

- Added an explicit registry of expected final years and the canonical OSPI SAFS landing page.
- Restricted discovery to authoritative OSPI hosts and supported S-275 file formats.
- Added Python discovery with retry/backoff and an explicit user agent.
- Added provenance fields for school year, source page, direct URL, format, retrieval timestamp, SHA-256, byte size, HTTP metadata, and parser/schema version.
- Added detection for missing expected years and HTML/error responses masquerading as data files.
- Added representative unit tests.
- Added a GitHub Actions workflow for PR/manual/weekly source discovery checks.

## Scope boundary

Full immutable downloads, source-file hashing during collection, and artifact retention are implemented in Plan 02. Plan 01 establishes and validates discovery/provenance mechanics.

## Acceptance

The workflow reports the expected annual S-275 sources and fails clearly if an expected source cannot be discovered.
