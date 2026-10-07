# Rebuild and future-year updates

## Rebuild the accepted analysis

The existing **Analyze retained sources** workflow rebuilds the current accepted period, including the generated report, without contacting OSPI for the retained workbook inputs. Select both immutable snapshot tags explicitly:

```sh
gh workflow run analyze-snapshot.yml --repo jschell/rsd407-pay --ref main \
  -f snapshot_tag=s275-source-2026-10-02 \
  -f normalization_tag=normalization-source-2026-10-04
```

Use the resulting retained-analysis artifact for normalized data, reconciliation evidence, and the generated Markdown/CSV report. This command rebuilds; it does not publish a release or update the committed report automatically.

## Monitor newly final workbook candidates

The weekly/manual **S-275 source check** captures the official source page and runs `rsd407_pay.final_source_watch`. Its JSON lists explicitly final personnel-workbook links outside accepted coverage. It excludes preliminary/draft labels and non-workbook links. A lack of candidates is not proof that newer final data do not exist; differently labeled sources require review.

Reproduce discovery from retained HTML:

```sh
PYTHONPATH=src python -m rsd407_pay.final_source_watch \
  --html artifacts/s275-source-page.html
```

The captured page hash, link labels, URLs, and capture time are retained with the workflow artifact. Artifact retention is temporary; a reviewed update must preserve the accepted source/revision evidence durably.

## Promote a future year

Candidate discovery does not change the accepted dataset. Before a year can enter the report, validate source identity/finality and schema, capture it under a new immutable tag, obtain matching enrollment/CPI data and personnel controls, update the shared accepted period, and pass the entire analysis and report-generation workflow.

The shared registry and coverage gate synchronize accepted years across analysis inputs. Merely adding a year to `config/sources.json` is insufficient: new source captures and controls still require reviewed updates before future-year promotion is supported.

Never overwrite historical release captures. An upstream revision requires a new capture, a comparison with the accepted source, and a recorded effect on the report.

## Historical workbook revisions

The weekly/manual source check downloads `collection.json` from the explicit `accepted_snapshot_tag` in `config/sources.json`, then checks current workbook bytes for every accepted year. The baseline is not automatically selected from the latest release.

`source-revisions.json` distinguishes content revisions, URL relocations, unchanged bytes, and failed observations. Each failure is retained while later years are still attempted. Revised workbook bytes are captured under `artifacts/source-revisions/YEAR/SHA256.xlsx` (or `.xls`); existing accepted workbooks are untouched.

A revision or failed observation makes this monitoring check fail so that review is visible. The retained-source analysis remains reproducible from its original immutable release. Review the artifact before deciding whether to create a new accepted capture.

Reproduce with the retained accepted manifest:

```sh
PYTHONPATH=src python -m rsd407_pay.source_revisions \
  --baseline artifacts/manifests/accepted-collection.json
```

The monitor verifies workbook identity and byte hashes; it does not establish the effect of a revision on Riverview results. Changed-source artifacts are temporary evidence. Plan 09 still needs durable reviewed revision publication and before/after analytical comparisons.

## Accepted-period contract and coverage gate

`config/sources.json` defines the ordered, contiguous accepted school years. Analysis modules share that registry; findings use its first and last years. `rsd407_pay.coverage_gate` runs before S-275 normalization and rejects mismatched or duplicate snapshot/enrollment/Access years, preliminary scope, missing CPI ending years (including the 2025 dollar base), and missing or unaccepted published controls for accepted years from 2019-20 onward. Earlier independent controls remain unavailable.

The registry alone still cannot promote a new year: new normalization captures and controls require reviewed updates; the dollar base remains explicitly fixed at 2025. Historical evidence and existing results remain tied to their immutable snapshot tags.

## Period-aware normalization capture and replay

CPI requests derive ending calendar years from the shared accepted period plus the explicit 2025 dollar base. Requests are split into nonoverlapping windows of at most ten years; filenames follow those windows. Normalization manifests include the raw paths declared by the derived CPI capture, and replay reads only those hash-verified inputs. Duplicate BLS observations or missing periodic observations fail; the documented October 2025 exception remains limited to that year.

Enrollment discovery accepts exactly one official HTTPS final `.xlsx` summary whose stated year range covers the entire accepted period. Changed endpoints are supported; preliminary labels, insufficient ranges, invalid ranges, foreign hosts, and ambiguous matches fail. Extraction still checks required sheets and Riverview identity.

The dollar base stays at 2025 deliberately: adding a school year does not silently rebase historical results or change output field names. Accepted inputs and published results are unchanged. Future-year tests are synthetic dependency/coverage checks; full retained-source CI validates the actual accepted historical capture. Durable revision publication and analytical before/after comparison remain outstanding under Plan 09.
