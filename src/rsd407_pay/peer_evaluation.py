"""Evaluate classification, scale and school-denominator sensitivity."""
import argparse
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path


def cost(row, include_directors=False):
    value=row['central_compensation']
    if include_directors: value+=row['director_supervisor_compensation_excluded']
    return value/row['student_fte']*1000


def gap(a,b): return (a/b-1)*100


def decomposition(a,b):
    # Symmetric two-factor allocation; terms sum exactly to the observed cost gap.
    af,bf=a['central_fte_per_1000_students'],b['central_fte_per_1000_students']
    ar,br=a['central_compensation_per_staff_fte'],b['central_compensation_per_staff_fte']
    return {'staffing_intensity_component':(af-bf)*(ar+br)/2,
            'compensation_per_staff_fte_component':(ar-br)*(af+bf)/2,
            'total_gap':cost(a)-cost(b),
            'interpretation':'Arithmetic decomposition, not causal attribution.'}


def evaluate(comparison,schools):
    if comparison.get('status')!='source_verified_comparison': raise RuntimeError('source-verified comparison required')
    latest=[r for r in comparison['rows'] if r['school_year']=='2024-25']
    if len({r['district'] for r in latest})!=len(latest): raise RuntimeError('duplicate district-year')
    by={r['district']:r for r in latest};rv=by['Riverview']
    peers=[r for d,r in by.items() if d!='Riverview' and .7*rv['student_fte']<=r['student_fte']<=1.3*rv['student_fte']]
    if len(peers)!=6: raise RuntimeError('review peer group: expected six enrollment-size peers')
    matching={}
    for label,include in [('strict',False),('all_directors_scenario',True)]:
        median=statistics.median(cost(r,include) for r in peers)
        matching[label]={'peer_median':median,'riverview':cost(rv,include),'riverview_gap_percent':gap(cost(rv,include),median)}
    classifications=[]
    for r in latest:
        classifications.append({'district':r['district'],'student_fte':r['student_fte'],
          'strict_cost_per_1000':cost(r),'with_all_directors_cost_per_1000':cost(r,True),
          'director_fte_excluded':r['director_supervisor_fte_excluded'],
          'director_compensation_excluded':r['director_supervisor_compensation_excluded']})
    denominators=[]
    for r in schools['rows']:
        counts=dict(Counter(s['currentschooltype'] for s in r['reporting_schools']))
        p=counts.get('P',0)
        if not p: raise RuntimeError('missing P-coded school denominator')
        denominators.append({'district':r['district'],'school_admin_fte':r['school_admin_fte'],
          'all_reporting_schools':r['reporting_school_count'],'school_type_counts':counts,
          'p_coded_schools':p,'fte_per_all_reporting_schools':r['school_admin_fte']/r['reporting_school_count'],
          'same_total_fte_per_p_coded_school':r['school_admin_fte']/p})
    comparisons=[]
    for d in ['Snoqualmie Valley','Northshore','Monroe']:
        comparisons.append({'district':d,'strict_gap_percent':gap(cost(rv),cost(by[d])),
          'all_directors_scenario_gap_percent':gap(cost(rv,True),cost(by[d],True)),
          'decomposition':decomposition(rv,by[d])})
    previous=next(r for r in comparison['rows'] if r['district']=='Riverview' and r['school_year']=='2023-24')
    return {'schema_version':1,'year':'2024-25','status':'descriptive_evaluation',
      'size_matching':{'rule':'2024-25 student FTE within +/-30% of Riverview; selected ten-district cohort only',
                      'districts':[r['district'] for r in peers],'results':matching},
      'nearby_comparisons':comparisons,'classification_sensitivity':classifications,
      'school_denominator_sensitivity':denominators,
      'riverview_latest_year':{'central_fte_before':previous['central_fte'],'central_fte_after':rv['central_fte'],
          'central_fte_change_percent':gap(rv['central_fte'],previous['central_fte']),
          'compensation_per_staff_fte_change_percent':gap(rv['central_compensation_per_staff_fte'],previous['central_compensation_per_staff_fte']),
          'student_fte_change_percent':gap(rv['student_fte'],previous['student_fte']),
          'nominal_cost_per_1000_change_percent':gap(cost(rv),cost(previous))},
      'limits':['Adding every Director/Supervisor is a consistent sensitivity scenario, not an established central-office total or statistical confidence bound.',
        'The P-only denominator retains the full school-admin FTE numerator; it is not staffing allocated to P schools and is not a physical-campus count.',
        'The six size peers are drawn from the selected nearby cohort, not all Washington districts; medians are descriptive, not statistical significance tests.',
        'Source year labels, program mix, services, outsourcing and independent peer reconciliation remain review requirements.',
        'Same-year CPI adjustment applies the same factor to these districts and does not change their relative ratios. Latest-year growth here is nominal.']}


def money(x): return f'${x:,.0f}'


def render(report):
    size=report['size_matching']['results'];by={r['district']:r for r in report['school_denominator_sensitivity']}
    lines=['# Evaluation of nearby district administration, 2024-25','',
      'The available evidence supports a finding of higher strict central-administration compensation per student than nearby larger districts. It does not establish excessive compensation, excessive staffing, or inefficiency. Classification and school-count choices materially affect comparisons.','',
      '## Enrollment-size peers','',report['size_matching']['rule']+'. The six peers are '+', '.join(report['size_matching']['districts'])+'.','',
      '| Classification | Riverview / 1,000 student FTE | Six-peer median / 1,000 | Riverview difference |',
      '| --- | --- | --- | --- |']
    for label,key in [('Strict central administration','strict'),('Strict plus every Director/Supervisor (scenario)','all_directors_scenario')]:
        r=size[key];lines.append(f"| {label} | {money(r['riverview'])} | {money(r['peer_median'])} | {r['riverview_gap_percent']:+.1f}% |")
    lines+=['','Riverview is not above the size-peer median on the strict measure. Including every Director/Supervisor reverses that relation. Actual functional allocation is required before describing a complete central-office cost.','',
      '## Nearby larger districts','',
      '| District | Riverview strict cost difference | Staffing-intensity component of dollar gap / 1,000 | Compensation-per-FTE component | Riverview difference with all directors |',
      '| --- | --- | --- | --- | --- |']
    for r in report['nearby_comparisons']:
        d=r['decomposition'];lines.append(f"| {r['district']} | {r['strict_gap_percent']:+.1f}% | {money(d['staffing_intensity_component'])} | {money(d['compensation_per_staff_fte_component'])} | {r['all_directors_scenario_gap_percent']:+.1f}% |")
    lines+=['','The components divide the observed strict cost gap symmetrically between staffing per student and compensation per admin FTE. They are an arithmetic decomposition, not causal estimates. For Northshore, Riverview has lower compensation per admin FTE; higher staffing per student accounts for the positive cost gap.','',
      '## School-count sensitivity','',
      'OSPI school-type codes distinguish P (Public School), A (Alternative), S (Special Education), and R (Reengagement). See the [official data dictionary](https://data.wa.gov/education/Washington-School-Improvement-Framework-WSIF-2024-/8v2t-vz3j). The denominator check below retains all school-admin FTE in both columns.','',
      '| District | All reporting schools | P-coded schools | FTE / all reporting schools | Same total FTE / P-coded school |',
      '| --- | --- | --- | --- | --- |']
    for name in ['Riverview','Snoqualmie Valley','Northshore','Monroe']:
        r=by[name];lines.append(f"| {name} | {r['all_reporting_schools']} | {r['p_coded_schools']} | {r['fte_per_all_reporting_schools']:.2f} | {r['same_total_fte_per_p_coded_school']:.2f} |")
    lines+=['','The earlier conclusion that Riverview has lower school-admin FTE per school than both Snoqualmie Valley and Northshore is conditional on counting all reporting programs. With the P-coded denominator, Riverview is approximately equal to Snoqualmie Valley and above Northshore. Neither denominator allocates administrators to actual campuses; a staffing/location crosswalk is needed to evaluate individual-school provision.','',
      '## Riverview latest-year change','']
    r=report['riverview_latest_year'];lines+=[f"Central-admin FTE increased from {r['central_fte_before']:.3f} to {r['central_fte_after']:.3f} ({r['central_fte_change_percent']:+.1f}%). Compensation per admin FTE changed {r['compensation_per_staff_fte_change_percent']:+.1f}%; student FTE changed {r['student_fte_change_percent']:+.1f}%. Nominal compensation per 1,000 student FTE changed {r['nominal_cost_per_1000_change_percent']:+.1f}%.",
      '', 'The latest increase reflects more reported central-admin FTE and fewer students. Average compensation per FTE fell. Vacancies, partial-year staffing, duties, and reclassification have not been resolved, so these are accounting drivers rather than established causes.','',
      '## Public-facing conclusion','',
      'Riverview’s strict central-administration compensation per student exceeds nearby larger districts, primarily reflecting higher reported staffing per student. It is close to the median of selected districts with similar enrollment. Including operational Director/Supervisor roles changes the size-peer comparison. School staffing comparisons depend on how alternative and program schools are counted. The evidence warrants reviewing duties and staffing changes; it does not support a finding of waste or overpayment.','',
      '## Evidence still needed','',
      '- Documented duty/assignment codes or district position descriptions to allocate directors by function consistently across districts.',
      '- A school/program-to-campus and administrator-location crosswalk, including shared assignments and outsourced services.',
      '- Same-year student needs, service responsibilities, and independent peer personnel reconciliation.',
      '- An explanation of Riverview’s central FTE change from 2023-24 to 2024-25 supported by staffing/position records.','',
      '## Provenance and reproduction','',
      'Generated from [comparison.json](comparison.json) and [school-administration.json](school-administration.json). [evaluation.json](evaluation.json) records input and evaluator hashes and all scenario values. Run `PYTHONPATH=src python -m rsd407_pay.peer_evaluation`. No raw captures or category assignments are changed.','']
    lines+=['- '+x for x in report['limits']]
    return '\n'.join(lines)+'\n'


def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--root',default='docs/comparisons');a=p.parse_args(argv);root=Path(a.root)
    paths=[root/'comparison.json',root/'school-administration.json'];data=[p.read_bytes() for p in paths]
    parsed=[json.loads(x) for x in data]
    if parsed[1]['comparison_input_sha256']!=hashlib.sha256(data[0]).hexdigest():
        raise RuntimeError('school-count inputs do not match comparison hash')
    report=evaluate(*parsed);report['input_sha256']={p.name:hashlib.sha256(x).hexdigest() for p,x in zip(paths,data)}
    report['evaluation_code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (root/'evaluation.json').write_text(json.dumps(report,indent=2)+'\n');(root/'evaluation.md').write_text(render(report))
    print(json.dumps(report['size_matching']))
if __name__=='__main__':main()
