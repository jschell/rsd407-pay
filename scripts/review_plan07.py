"""Reproduce the aggregate Plan 07 evidence from retained analysis artifacts."""
import csv
import hashlib
import json
from pathlib import Path
from rsd407_pay.source_warning_review import summarize

root = Path('artifacts')
inputs = ['normalized/rsd407-job-family.csv', 'normalized/annual-metrics.json',
          'normalized/validation-report.json', 'reconciliation/table45b-reconciliation.json',
          'reconciliation/personnel-compensation-comparison.json',
          'reconciliation/access-extract-reconciliation.json']
metrics = json.loads((root/inputs[1]).read_text())
validation = json.loads((root/inputs[2]).read_text())
fte = json.loads((root/inputs[3]).read_text())
comp = json.loads((root/inputs[4]).read_text())
access = json.loads((root/inputs[5]).read_text())
with (root/inputs[0]).open(newline='') as h:
    rows = list(csv.DictReader(h))
annual = []
for year in sorted({r['school_year'] for r in rows}):
    subset = [r for r in rows if r['school_year'] == year]
    warning = summarize([{k: float(r[k] or 0) for k in
        ('certificated_fte', 'classified_fte', 'base_salary', 'total_salary')} for r in subset])
    salary = next(r['total_salary'] for r in metrics['district'] if r['school_year'] == year)
    annual.append(dict(school_year=year, **warning,
        zero_fte_salary_share=warning['zero_fte_total_salary']/salary,
        extract_source_hashes=sorted({r['source_sha256'] for r in subset})))
by = {r['school_year']: r for r in metrics['district']}
changes = []
for item in next(w['items'] for w in validation['warnings'] if w['check']=='large_year_over_year_changes'):
    field, start, end = item['field'], item['from'], item['to']
    categories = {(r['school_year'], r['job_family']): r for r in metrics['categories']}
    families = sorted({r['job_family'] for r in metrics['categories']})
    parts = {f: categories.get((end,f),{}).get(field,0)-categories.get((start,f),{}).get(field,0) for f in families}
    total = by[end][field]-by[start][field]
    if abs(sum(parts.values())-total)>0.01:
        raise RuntimeError('category decomposition does not reproduce district change')
    component_fields = ['total_salary','insurance_benefits','mandatory_benefits'] if field=='reported_employer_compensation' else [field]
    components = {k: by[end][k]-by[start][k] for k in component_fields}
    fte_ratio = by[end]['total_fte']/by[start]['total_fte']
    intensity_ratio = (by[end][field]/by[end]['total_fte'])/(by[start][field]/by[start]['total_fte'])
    changes.append(dict(item, absolute_change=total, components=components,
        category_contributions=parts, fte_growth=fte_ratio-1,
        compensation_per_fte_growth=intensity_ratio-1,
        interpretation='Exact accounting decomposition; not causal attribution.'))
report = {'schema_version':1, 'analysis_run_id':37406368550,
    'source_snapshots':{'s275':'s275-source-2026-10-02','normalization':'normalization-source-2026-10-04'},
    'input_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in inputs},
    'validation_status':validation['status'], 'access_status':access['status'],
    'annual_warnings':annual, 'large_changes':changes,
    'published_fte':fte['years'], 'published_compensation':comp['years'],
    'limitations':['Source-warning corroboration CI must pass before closeout.',
        'Individual payroll causes are not established.',
        'Published total salary and benefits remain semantic-review measures.',
        'Independent annual published controls unavailable before 2019-20.']}
Path('docs/evidence/plan07-review.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Plan 07 evidence review', '',
    'Aggregate evidence from [retained analysis run 37406368550](https://github.com/jschell/rsd407-pay/actions/runs/37406368550).', '',
    'Regenerate with `PYTHONPATH=src python -m rsd407_pay.access_extract_reconcile`, then `PYTHONPATH=src python scripts/review_plan07.py` from the repository root after downloading that run’s artifact into `artifacts/`. Input hashes and complete numeric comparisons are in [the machine-readable evidence](evidence/plan07-review.json).', '',
    '## Access-to-extract reconciliation', '',
    'All twelve years match employee-row counts and base salary, total salary, insurance, mandatory benefits, and employer compensation exactly. Maximum FTE difference is '+str(max(abs(r['measures']['total_fte']['difference']) for r in access['years']))+' FTE, within the existing Access verifier’s 0.000001 FTE allowance. This is a same-S-275-system cross-check, not independent validation. Component certificated/classified FTE are not separately registered in the accepted controls.', '',
    '## Warning review', '',
    'These employee-year rows remain in the source totals. The table quantifies the effect of zero-FTE rows on total salary; the salary gap is base minus total among salary-below-base rows, not a demonstrated underpayment. Conditions can overlap. Counts are employee-year rows, not distinct people across twelve years.', '',
    '| Year | Zero-FTE rows | Their total salary | Share of annual salary | Salary below base rows | Aggregate base-minus-total gap |',
    '|---|---:|---:|---:|---:|---:|']
for r in annual:
    lines.append(f"| {r['school_year']} | {r['zero_fte_rows']} | ${r['zero_fte_total_salary']:,.0f} | {r['zero_fte_salary_share']:.2%} | {r['salary_below_base_rows']} | ${r['salary_below_base_gap']:,.0f} |")
lines += ['', 'The PR source-warning job replays the retained SHA-identified Access databases and checks these four diagnostics against normalized results in every year. Its output establishes whether the conditions originate in the reporting source; it does not establish individual payroll explanations. No compensation is imputed or silently removed.', '', '## Annual changes', '',
    'The following decomposes flagged nominal increases into recorded components. Neither this accounting decomposition nor passing reconciliation establishes a cause such as a contract change.', '',
    '| Period | Measure | Increase | Percent | Components |', '|---|---|---:|---:|---|']
for r in changes:
    parts='; '.join(f'{k}: ${v:,.0f}' for k,v in r['components'].items())
    lines.append(f"| {r['from']} to {r['to']} | {r['field']} | ${r['absolute_change']:,.0f} | {r['percent_change']:.2%} | {parts} |")
lines += ['', 'The JSON also includes exact job-family contributions and FTE-versus-compensation-per-FTE growth for each change.', '', '## Independent published controls', '',
    'Personnel Summary Table 45B FTE and base salary pass for all six available years, 2019-20 through 2024-25. Exact published comparisons, source hashes, and display-rounding bounds are preserved in the JSON; reviewed pages and literal compensation rows are in `controls/personnel-summary-published.json`.', '',
    'Total salary, insurance, and mandatory benefits remain unresolved semantic comparisons. In 2024-25, the extract is $2,828,198.43 below implied published total salary, $233,409.07 below insurance, and $483,813.76 below mandatory benefits. These are material limitations. They are not given arbitrary tolerances or represented as independently validated. The exact match with Access supports faithful simplified-extract aggregation, not equivalence with every published measure.', '',
    'Annual independent published control coverage for 2013-14 through 2018-19 remains unavailable. Those years pass internal and same-system checks only.', '',
    '## Closeout boundary', '',
    'Plan 07 remains active until the new source-warning corroboration and complete PR analysis pass and the source-condition limitations are accepted in the completion record. No claim of payroll correctness, independent twelve-year compensation validation, or explanation of individual compensation is made.']
Path('docs/plan07-evidence-review.md').write_text('\n'.join(lines)+'\n')
