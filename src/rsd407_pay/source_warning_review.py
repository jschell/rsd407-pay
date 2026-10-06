"""Aggregate-only corroboration of warning conditions in retained Access sources."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
from .validation import YEARS

SUMMARY_FIELDS = ('zero_fte_rows', 'zero_fte_total_salary',
                  'salary_below_base_rows', 'salary_below_base_gap')

def summarize(rows):
    zero = [r for r in rows if r['certificated_fte'] + r['classified_fte'] == 0]
    below = [r for r in rows if r['total_salary'] < r['base_salary']]
    return {'zero_fte_rows': len(zero),
            'zero_fte_total_salary': sum(r['total_salary'] for r in zero),
            'salary_below_base_rows': len(below),
            'salary_below_base_gap': sum(r['base_salary']-r['total_salary'] for r in below)}

def access_rows(db, table):
    process = subprocess.Popen(['mdb-export', str(db), table], stdout=subprocess.PIPE,
                               text=True)
    rows = []
    try:
        for row in csv.DictReader(process.stdout):
            if row.get('codist', '').strip() != '17407' or row.get('recno', '').strip() != '1':
                continue
            number = lambda field: float(row.get(field) or 0)
            rows.append({'certificated_fte': number('certfte'),
                'classified_fte': number('clasfte'),
                'base_salary': number('certbase') + number('clasbase'),
                'total_salary': number('tfinsal')})
    finally:
        process.stdout.close()
        code = process.wait()
    if code:
        raise RuntimeError(f'mdb-export failed with {code}')
    return rows

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--evidence', default='access-evidence')
    p.add_argument('--rows', default='artifacts/normalized/rsd407-job-family.csv')
    p.add_argument('--controls', default='controls/s275-access-riverview.json')
    p.add_argument('--output', default='artifacts/reconciliation/source-warning-review.json')
    a = p.parse_args(argv)
    evidence = Path(a.evidence)
    schema = json.loads((evidence/'s275-access-schema-inventory.json').read_text())
    controls = json.loads(Path(a.controls).read_text())
    accepted = {r['school_year']: r for r in controls['years']}
    with Path(a.rows).open(newline='') as h:
        extract = list(csv.DictReader(h))
    results, errors = [], []
    if sorted(r['school_year'] for r in schema['resources']) != YEARS:
        errors.append('Access evidence must cover exactly twelve years')
    for source in schema['resources']:
        year = source['school_year']
        db = evidence/'raw/s275-access'/year/source['database_file']
        digest = hashlib.file_digest(db.open('rb'), 'sha256').hexdigest()
        if digest != accepted[year]['database_sha256']:
            errors.append(f'{year}: database hash differs from accepted source')
            continue
        source_summary = summarize(access_rows(db, accepted[year]['table']))
        normalized_summary = summarize([{k: float(r[k] or 0) for k in
            ('certificated_fte', 'classified_fte', 'base_salary', 'total_salary')}
            for r in extract if r['school_year'] == year])
        differences = {k: normalized_summary[k]-source_summary[k] for k in SUMMARY_FIELDS}
        if any(differences.values()):
            errors.append(f'{year}: source warning diagnostics differ')
        results.append({'school_year': year, 'source_url': source['url'],
            'database_sha256': digest, 'source_sha256': source['source_sha256'],
            'extract': normalized_summary, 'access': source_summary,
            'differences': differences})
    report = {'schema_version': 1, 'status': 'fail' if errors else 'pass',
        'errors': errors, 'years': results,
        'limitation': 'Same-system aggregate corroboration establishes source conditions; it does not identify payroll causes or validate individual compensation.'}
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
