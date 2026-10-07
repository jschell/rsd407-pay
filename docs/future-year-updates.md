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

The current code still contains fixed 2013-14 through 2024-25 assumptions. Merely adding a year to `config/sources.json` is insufficient. Plan 09 will replace those assumptions and add historical source-hash/revision comparisons before future-year promotion is supported.

Never overwrite historical release captures. An upstream revision requires a new capture, a comparison with the accepted source, and a recorded effect on the report.
