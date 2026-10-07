"""Generate aggregate longitudinal tables and narrative from gated outputs."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from .validation import YEARS

MONEY = ('base_salary', 'total_salary', 'reported_employer_compensation')
CPI = ('national_cpi_u', 'seattle_cpi_u')

def pct(first, last):
    return (last/first-1)*100 if first else None

def fmt(value, money=False):
    if value is None:
        return 'not defined'
    return f'${value:,.0f}' if money else f'{value:,.2f}'

def table(headers, rows):
    return ['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |',
            *['| '+' | '.join(str(v).replace('|','/') for v in row)+' |' for row in rows]]

def require_gate(report, label):
    if report.get('status') != 'pass':
        raise RuntimeError(f'{label} must pass before publishing')

def category_changes(metrics, normalized):
    norm = {r['school_year']: r for r in normalized['years']}
    by = {(r['school_year'], r['job_family']): r for r in metrics['categories']}
    out = []
    for family in sorted({r['job_family'] for r in metrics['categories']}):
        a, b = by.get((YEARS[0], family)), by.get((YEARS[-1], family))
        if a is None or b is None:
            raise RuntimeError(f'{family}: baseline or latest category missing')
        intensity_a = a['total_fte']/norm[YEARS[0]]['student_fte']*1000
        intensity_b = b['total_fte']/norm[YEARS[-1]]['student_fte']*1000
        out.append({'job_family': family, 'baseline_employee_rows': a['employee_rows'],
            'latest_employee_rows': b['employee_rows'], 'baseline_fte': a['total_fte'],
            'latest_fte': b['total_fte'], 'fte_change': b['total_fte']-a['total_fte'],
            'baseline_fte_per_1000_students': intensity_a,
            'latest_fte_per_1000_students': intensity_b,
            'intensity_change': intensity_b-intensity_a,
            'nominal_total_salary_change': b['total_salary']-a['total_salary']})
    return out

def build(metrics, normalized, validation, access, published_fte, published_compensation):
    for label, report in [('internal validation', validation), ('Access reconciliation', access),
                          ('published FTE', published_fte), ('published base salary', published_compensation)]:
        require_gate(report, label)
    if validation.get('critical'):
        raise RuntimeError('critical validation failures remain')
    for label, rows in [('district', metrics['district']), ('normalized', normalized['years'])]:
        if sorted(r['school_year'] for r in rows) != YEARS:
            raise RuntimeError(f'{label}: exact twelve-year coverage required')
    district = {r['school_year']: r for r in metrics['district']}
    norm = {r['school_year']: r for r in normalized['years']}
    annual = []
    for year in YEARS:
        d, n = district[year], norm[year]
        if n['student_fte'] <= 0:
            raise RuntimeError(f'{year}: enrollment must be positive')
        annual.append(dict(school_year=year,
            **{k:d[k] for k in ('employee_rows','certificated_fte','classified_fte','total_fte',
                'base_salary','total_salary','insurance_benefits','mandatory_benefits','reported_employer_compensation')},
            student_fte=n['student_fte'], staff_fte_per_1000_students=n['staff_fte_per_1000_student_fte'],
            classified_share_of_fte=d['classified_fte']/d['total_fte'],
            zero_fte_rows=d['zero_fte_rows'], salary_below_base_rows=d['total_salary_below_base_rows']))
    return annual, category_changes(metrics, normalized)

def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='artifacts')
    parser.add_argument('--output-dir', default='artifacts/reporting')
    parser.add_argument('--analysis-ref', required=True)
    parser.add_argument('--analysis-run', default='not recorded')
    a = parser.parse_args(argv)
    root, out = Path(a.root), Path(a.output_dir)
    names = {'metrics':'normalized/annual-metrics.json', 'normalized':'normalized/normalized-metrics.json',
        'validation':'normalized/validation-report.json', 'access':'reconciliation/access-extract-reconciliation.json',
        'published_fte':'reconciliation/table45b-reconciliation.json',
        'published_compensation':'reconciliation/personnel-compensation-comparison.json',
        'admin':'normalized/admin-overhead.json', 'findings':'normalized/longitudinal-findings.json'}
    payload = {k:json.loads((root/v).read_text()) for k,v in names.items()}
    annual, changes = build(**{k:payload[k] for k in ('metrics','normalized','validation','access','published_fte','published_compensation')})
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out/'annual-summary.csv', annual)
    write_csv(out/'baseline-category-changes.csv', changes)
    metrics, norm = payload['metrics'], {r['school_year']:r for r in payload['normalized']['years']}
    category_rows=[]
    for row in metrics['categories']:
        category_rows.append(dict(school_year=row['school_year'], job_family=row['job_family'],
            employee_rows=row['employee_rows'], total_fte=row['total_fte'],
            fte_per_1000_student_fte=row['total_fte']/norm[row['school_year']]['student_fte']*1000,
            **{k:row[k] for k in MONEY}))
    write_csv(out/'annual-category-detail.csv', category_rows)
    real=[]
    for year in YEARS:
        for series in CPI:
            r=norm[year]['constant_2025_dollars'][series]
            real.append(dict(school_year=year, cpi_series=series, **{k:r[k] for k in MONEY},
                **{k+'_per_student_fte':r[k+'_per_student_fte'] for k in MONEY}))
    write_csv(out/'annual-real-compensation.csv',real)
    manifest={'schema_version':1, 'period':{'start':YEARS[0],'end':YEARS[-1]},
        'analysis_ref':a.analysis_ref, 'analysis_run':a.analysis_run,
        'source_snapshots':payload['findings']['source_snapshots'],
        'input_sha256':{v:hashlib.sha256((root/v).read_bytes()).hexdigest() for v in names.values()},
        'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'gate_status':'pass', 'limitations':'See report.md; employer compensation is not operating expenditure.'}
    (out/'report-provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
    first,last=annual[0],annual[-1]
    lines=['# Riverview staffing and compensation, '+YEARS[0]+' through '+YEARS[-1], '',
        'This report describes the final public S-275 extract. Counts are employee-year rows and FTE; they are not counts of assignments or unique people across years.', '',
        '## What changed', '',
        f"Student FTE changed from {fmt(first['student_fte'])} to {fmt(last['student_fte'])} ({pct(first['student_fte'],last['student_fte']):+.1f}%). Staff FTE changed from {fmt(first['total_fte'])} to {fmt(last['total_fte'])} ({pct(first['total_fte'],last['total_fte']):+.1f}%). Staff FTE per 1,000 student FTE changed from {fmt(first['staff_fte_per_1000_students'])} to {fmt(last['staff_fte_per_1000_students'])} ({pct(first['staff_fte_per_1000_students'],last['staff_fte_per_1000_students']):+.1f}%).", '',
        'These changes describe staffing intensity and compensation. They do not establish necessity, efficiency, service quality, or causes.', '',
        '## Validation and limitations', '',
        '- Twelve-year Access headcount and registered compensation checks pass; these are same-S-275-system cross-checks.',
        '- Independent published FTE and base salary pass for 2019-20 through 2024-25 only. Earlier independent annual reports are unavailable.',
        '- Published total salary and benefits remain unresolved semantic comparisons. Extract totals are reproduced faithfully but are not independently validated against those published measures.',
        '- Zero-FTE and salary-below-base conditions are preserved. Direct Access replay corroborated their counts and amounts in all twelve years in run 37408082579; individual payroll causes remain unknown.',
        '- Duty Title defines job family. Director/Supervisor stays outside strict central administration because operating function is not identified. See the repository category-definition document.',
        '- The sharp change in zero-FTE reporting in 2024-25 limits interpretation of employee-row trends. No correction or causal claim is made.',
        '- The 2019-20 P-223 source combines actual enrollment through March with projected April-June and summer values.',
        '- Inflation maps each school year to its ending calendar year; amounts are expressed in constant 2025 dollars with national and Seattle CPI-U separately.',
        '- Employer compensation is reported personnel compensation, not total district or administrative operating expenditure.', '',
        '## Annual district summary', '']
    lines+=table(['Year','Employee rows','Student FTE','Staff FTE','Staff / 1,000 students','Base salary','Total salary','Employer compensation'],
        [[r['school_year'],r['employee_rows'],fmt(r['student_fte']),fmt(r['total_fte']),fmt(r['staff_fte_per_1000_students']),*[fmt(r[k],True) for k in MONEY]] for r in annual])
    lines+=['', 'Detailed certificated/classified FTE, insurance, mandatory benefits, and warning counts are in [annual-summary.csv](annual-summary.csv).', '',
        '## Job-family changes', '', 'Baseline versus latest; annual category counts, FTE, and compensation are in [annual-category-detail.csv](annual-category-detail.csv).', '']
    lines+=table(['Job family','Baseline rows','Latest rows','Baseline FTE','Latest FTE','FTE change','Change in FTE / 1,000 students'],
        [[r['job_family'],r['baseline_employee_rows'],r['latest_employee_rows'],fmt(r['baseline_fte']),fmt(r['latest_fte']),fmt(r['fte_change']),fmt(r['intensity_change'])] for r in changes])
    lines+=['', '## Nominal and real compensation', '',
        'All amounts below are per student FTE. The CSV provides every year’s real totals and per-student amounts for both CPI series.', '']
    money_rows=[]
    for key in MONEY:
        for series in ['nominal',*CPI]:
            def value(year):
                return norm[year][key+'_per_student_fte'] if series=='nominal' else norm[year]['constant_2025_dollars'][series][key+'_per_student_fte']
            x,y=value(YEARS[0]),value(YEARS[-1]);money_rows.append([key,series,fmt(x,True),fmt(y,True),f'{pct(x,y):+.1f}%'])
    lines+=table(['Measure','Dollar basis','Baseline','Latest','Change'],money_rows)
    lines+=['', 'See [annual-real-compensation.csv](annual-real-compensation.csv) for complete annual series.', '',
        '## Instruction, administration, and classified staffing', '',
        'Compare both the size of each group and its enrollment-adjusted intensity. These category-based views are not budgets or assignment-level cost allocations.', '']
    fams={r['job_family'] for r in changes}
    instructional={'teachers','other certificated instructional','paraeducators/instructional aides'} & fams
    # Mixed occupational support groups are kept separate; the exact title mapping remains authoritative.
    groups={'instructional roles (listed categories)':instructional,
            'school administration':{'principals/APs'},'strict central administration':{'district/central administration'}}
    by={(r['school_year'],r['job_family']):r for r in metrics['categories']}
    comparison=[]
    for group,families in groups.items():
        if not families or any((year,f) not in by for year in YEARS for f in families):
            raise RuntimeError(f'{group}: required category coverage missing')
        x=sum(by[(YEARS[0],f)]['total_fte'] for f in families)
        y=sum(by[(YEARS[-1],f)]['total_fte'] for f in families)
        comparison.append([group,', '.join(sorted(families)),fmt(x),fmt(y),fmt(x/first['student_fte']*1000),fmt(y/last['student_fte']*1000)])
    comparison.append(['all classified FTE','Source classified FTE; overlaps occupational groups',fmt(first['classified_fte']),fmt(last['classified_fte']),fmt(first['classified_fte']/first['student_fte']*1000),fmt(last['classified_fte']/last['student_fte']*1000)])
    lines+=table(['Group','Definition','Baseline FTE','Latest FTE','Baseline / 1,000','Latest / 1,000'],comparison)
    lines+=['', f"Classified share of total FTE changed from {first['classified_share_of_fte']:.1%} to {last['classified_share_of_fte']:.1%}.", '',
        '## Source and reproduction appendix', '',
        f"Analysis code reference: `{a.analysis_ref}`. Analysis run: `{a.analysis_run}`.",
        f"Immutable snapshots: `{manifest['source_snapshots']['s275']}` and `{manifest['source_snapshots']['normalization']}`.", '',
        '- OSPI S-275 and Access landing page: https://ospi.k12.wa.us/safs-data-files',
        '- OSPI independent Personnel Summary Reports: https://ospi.k12.wa.us/policy-funding/school-apportionment/school-publications/personnel-summary-reports',
        '- Official year-specific Access URLs and hashes: `controls/s275-access-riverview.json`.',
        '- Published controls, URLs, source hashes, pages, and literal source rows: `controls/personnel-summary-published.json`.',
        '- Enrollment and CPI source identity/hashes: immutable normalization snapshot and `config/normalization-sources.json`.',
        '- Warning verification and accepted interpretation boundaries: `docs/plan07-evidence-review.md`.', '',
        'Every input file used here is SHA-identified in [report-provenance.json](report-provenance.json). Run `python -m rsd407_pay.reporting --analysis-ref COMMIT --analysis-run RUN_ID` with `PYTHONPATH=src` after the retained-source analysis; the workflow generates this report automatically. Analytical numbers are generated from the output files, never edited in the narrative.']
    (out/'report.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
    main()
