# Plan 02 — S-275 collection workflow

## Goal

Use Python in GitHub Actions to download and cache authoritative annual S-275 files reproducibly.

## Work

- Implement Python CLI commands such as:
  - `python -m rsd407_pay sources check`
  - `python -m rsd407_pay collect --year 2024-25`
  - `python -m rsd407_pay collect --all-final`
- Store immutable raw files outside generated analytical tables.
- Use GitHub Actions artifacts for large/raw downloads when repository storage would be inappropriate.
- Store hashes/manifests in git even when raw files are artifact-only.
- Support manual dispatch by school year and full historical rebuild.
- Add scheduled source check for newly finalized OSPI data, without automatically mixing preliminary data into the final series.
- Pin Python/dependencies and use deterministic parsing.

## GitHub Actions

Create workflows for:

1. source validation;
2. one-year collection;
3. all-final historical collection;
4. test/lint validation.

## Acceptance

A clean workflow runner can collect an annual source, verify its hash/type, produce a manifest, and expose the raw file as an artifact without manual browser intervention.
