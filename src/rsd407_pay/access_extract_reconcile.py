"""Compare the normalized extract with accepted same-system Access controls."""
import argparse
import json
from pathlib import Path
from .validation import YEARS

FIELDS = {'personnel_rows': 'employee_rows', 'total_fte': 'total_fte',
          'base_salary': 'base_salary', 'total_salary': 'total_salary',
          'insurance': 'insurance_benefits', 'mandatory_benefits': 'mandatory_benefits',
          'reported_employer_compensation': 'reported_employer_compensation'}
# Matches the existing Access regeneration verifier's floating-point allowance.
FTE_TOLERANCE = 1e-6

def reconcile(controls, metrics):
    errors = []
    if controls.get('district_code') != '17407':
        errors.append('accepted control district must be 17407')
    expected = controls.get('years', [])
    actual = metrics.get('district', [])
    for label, rows in [('controls', expected), ('metrics', actual)]:
        years = [r['school_year'] for r in rows]
        if sorted(years) != YEARS:
            errors.append(f'{label}: exact twelve-year coverage required; got {years}')
    by = {r['school_year']: r for r in actual}
    comparisons = []
    for control in expected:
        year = control['school_year']
        if year not in by:
            continue
        measures = {}
        for key, field in FIELDS.items():
            observed, accepted = by[year][field], control[key]
            difference = observed - accepted
            tolerance = FTE_TOLERANCE if key == 'total_fte' else 0
            ok = abs(difference) <= tolerance
            measures[key] = {'extract': observed, 'access': accepted,
                'difference': difference, 'tolerance': tolerance,
                'status': 'pass' if ok else 'fail'}
            if not ok:
                errors.append(f'{year}: {key} differs by {difference}')
        comparisons.append({'school_year': year, 'measures': measures,
            'source_url': control.get('source_url'),
            'source_sha256': control['source_sha256'],
            'database_sha256': control['database_sha256'], 'table': control['table']})
    return {'schema_version': 1, 'district_code': '17407',
        'source_class': 's275_access', 'independence': 'same_system_cross_check',
        'status': 'fail' if errors else 'pass', 'errors': errors, 'years': comparisons}

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--controls', default='controls/s275-access-riverview.json')
    parser.add_argument('--metrics', default='artifacts/normalized/annual-metrics.json')
    parser.add_argument('--output', default='artifacts/reconciliation/access-extract-reconciliation.json')
    args = parser.parse_args(argv)
    report = reconcile(json.loads(Path(args.controls).read_text()),
                       json.loads(Path(args.metrics).read_text()))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'errors': report['errors']}))
    if report['status'] != 'pass':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
