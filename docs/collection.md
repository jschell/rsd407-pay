# S-275 collection

Raw OSPI personnel files are collected by GitHub Actions and are not committed to git.

Run **Collect S-275** with a final `school_year` such as `2024-25`, or set `all_final=true`. The workflow discovers the authoritative OSPI URL, rejects HTML/error responses, calculates SHA-256 and byte size, writes a JSON manifest, and uploads the raw files plus manifest as an Actions artifact.

Raw paths are `artifacts/raw/<school-year>/s275.<format>`. Existing raw content with a different hash is never overwritten, making a changed historical OSPI source an explicit revision event.

Artifacts are retained for 30 days. The source URL and cryptographic manifest provide the reproducibility record; later plans can publish stable manifests without committing large personnel files.
