# Longitudinal findings

The [generated report](reporting/report.md) is the current narrative and table view. It includes annual staffing and compensation, job-family changes, both inflation series, and central-administration compensation per 1,000 student FTE.

All analytical numbers are generated from gated retained-analysis outputs. [Report provenance](reporting/report-provenance.json) records immutable snapshot tags, input hashes, analysis reference, and generator hash. The report carries [Plan 07's limitations](plan07-evidence-review.md), including missing earlier independent annual controls and unresolved published total-salary/benefit semantics.

Regenerate with `PYTHONPATH=src python -m rsd407_pay.reporting --analysis-ref COMMIT --analysis-run RUN_ID` after the retained-source analysis. The workflow generates and uploads the report automatically.
