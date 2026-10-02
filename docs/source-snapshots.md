# S-275 source snapshots

Raw OSPI workbooks are immutable inputs but are too large for ordinary Git history. The project therefore retains validated captures as immutable GitHub Release assets.

## Publish once

Run **Publish S-275 source snapshot** with a new tag such as `s275-source-2026-10-02`. The workflow recollects all registered final years, validates workbook identity and hashes, builds `s275-source-snapshot.tar.gz`, and publishes the archive plus manifests. An existing tag is never overwritten.

## Reuse

Run **Analyze S-275 snapshot** with that tag. It downloads the retained archive, verifies every raw file against the snapshot metadata, and performs normalization and derived reporting without contacting OSPI.

## Refresh

A refresh is deliberate: publish a new snapshot tag. Upstream changes therefore create a new immutable capture instead of silently changing historical analytical inputs.

Small derived metadata and mapping definitions belong in Git. Large source workbooks do not.
