"""Reject partial period updates before deriving staffing or reports."""
import argparse
import json
from pathlib import Path
from .period import YEARS, require_coverage


def check(collection, enrollment, cpi, access, published, years=YEARS):
    errors = []
    expected_published = [y for y in years if int(y[:4]) >= 2019]
    for label, rows, expected in (
        ('S-275 snapshot', collection['sources'], years),
        ('enrollment', enrollment['years'], years),
        ('Access controls', access['years'], years),
        ('published controls', published['years'], expected_published),
    ):
        try:
            require_coverage(rows, expected, label)
        except RuntimeError as exc:
            errors.append(str(exc))
    if collection.get('release_scope') != 'final':
        errors.append('S-275 snapshot must be final')
    for control in published['years']:
        if control.get('review_status') != 'accepted':
            errors.append(f"{control['school_year']}: published control is not accepted")
    required_cpi = {str(int(y[:4]) + 1) for y in years} | {'2025'}
    for name in ('national_cpi_u', 'seattle_cpi_u'):
        values = cpi.get('series', {}).get(name, {}).get('values', {})
        missing = sorted(required_cpi - set(values))
        if missing:
            errors.append(f'{name}: missing CPI years {missing}')
    return {'schema_version': 1, 'status': 'fail' if errors else 'pass',
            'accepted_years': years, 'required_published_years': expected_published,
            'base_dollar_year': 2025, 'errors': errors}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='artifacts/reconciliation/accepted-period-coverage.json')
    a = p.parse_args(argv)
    load = lambda path: json.loads(Path(path).read_text())
    report = check(load('artifacts/manifests/collection.json'),
                   load('artifacts/normalization/enrollment.json'),
                   load('artifacts/normalization/cpi.json'),
                   load('controls/s275-access-riverview.json'),
                   load('controls/personnel-summary-published.json'))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
    if report['errors']:
        raise SystemExit('accepted-period coverage failed')


if __name__ == '__main__':
    main()
