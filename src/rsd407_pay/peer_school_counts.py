"""Add same-year reporting-school counts to the retained staffing comparison."""
import argparse
import hashlib
import json
import csv
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

API='https://data.wa.gov/resource/2rwv-gs2e.json'


def enrich(report, schools):
    latest=[r for r in report['rows'] if r['school_year']=='2024-25']
    by={}
    for s in schools:
        key=(s['districtcode'],s['schoolcode'])
        if key in by: raise RuntimeError(f'duplicate reporting school: {key}')
        by[key]=s
    result=[]
    for r in latest:
        members=[s for (code,_),s in by.items() if code==r['district_code']]
        if not members: raise RuntimeError(f"missing school count: {r['district']}")
        item=dict(r);item['reporting_school_count']=len(members)
        item['school_admin_fte_per_reporting_school']=r['school_admin_fte']/len(members)
        item['central_admin_fte_per_reporting_school']=r['central_fte']/len(members)
        item['reporting_schools']=sorted(members,key=lambda x:x['schoolcode'])
        result.append(item)
    return result


def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--root',default='artifacts/peer-comparison');p.add_argument('--schools-json');a=p.parse_args(argv)
    root=Path(a.root);report=json.loads((root/'comparison.json').read_text())
    codes=sorted({r['district_code'] for r in report['rows']})
    if any(not x.isdigit() for x in codes): raise RuntimeError('invalid district code')
    query={'$select':'distinct districtcode,districtname,schoolcode,schoolname,currentschooltype',
           '$where':"organizationlevel='School' AND schoolyear='2024-25' AND all_students>0 AND districtcode in ("+','.join("'"+c+"'" for c in codes)+')',
           '$order':'districtcode,schoolcode','$limit':'1000'}
    url=API+'?'+urlencode(query)
    if a.schools_json:
        data=Path(a.schools_json).read_bytes()
        provenance={'replayed_from':a.schools_json,'source_url':url}
    else:
        with urlopen(url,timeout=60) as response:data=response.read()
        provenance={'source_url':url,'retrieved_at':datetime.now(timezone.utc).isoformat()}
    schools=json.loads(data)
    if len(schools)>=1000: raise RuntimeError('school query may be truncated')
    result=enrich(report,schools)
    provenance.update(sha256=hashlib.sha256(data).hexdigest(),dataset='OSPI Report Card Enrollment 2024-25',school_year='2024-25')
    (root/'school-count-source.json').write_bytes(data)
    payload={'schema_version':1,'source':provenance,'rows':result,
             'comparison_input_sha256':hashlib.sha256((root/'comparison.json').read_bytes()).hexdigest(),
             'definition':'Distinct OSPI school codes with positive reported enrollment in 2024-25. Includes alternative/online/program schools; not a count of physical campuses.',
             'school_admin_definition':'School administrators in S-275: elementary/secondary principals, vice principals, and Other School Admin.; excludes central-office roles.'}
    (root/'school-administration.json').write_text(json.dumps(payload,indent=2)+'\n')
    fields=['district','student_fte','reporting_school_count','school_admin_fte','school_admin_fte_per_reporting_school','central_fte','central_admin_fte_per_reporting_school']
    with (root/'school-administration.csv').open('w',newline='') as h:
        w=csv.DictWriter(h,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(result)
    lines=['# School-administration staffing, 2024-25','',payload['definition'],'',payload['school_admin_definition'],'',
           '| District | Student FTE | Reporting schools | School-admin FTE | School-admin FTE / school | Central-admin FTE / school |',
           '| --- | --- | --- | --- | --- | --- |']
    for r in result:
        lines.append(f"| {r['district']} | {r['student_fte']:,.2f} | {r['reporting_school_count']} | {r['school_admin_fte']:.3f} | {r['school_admin_fte_per_reporting_school']:.2f} | {r['central_admin_fte_per_reporting_school']:.2f} |")
    lines+=['','Read alongside comparison.md: title categories do not establish full operating budgets or efficiency. School count includes programs that may share administration; physical-campus comparisons require a separate crosswalk.']
    (root/'school-administration.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'status':'pass','districts':len(result),'source_sha256':provenance['sha256']}))
if __name__=='__main__':main()
