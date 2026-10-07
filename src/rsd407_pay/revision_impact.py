"""Compare validated retained analyses and preserve reviewable evidence."""
import argparse
import hashlib
import json
import math
import re
import zipfile
from pathlib import Path

DATA = ('normalized/annual-metrics.json', 'normalized/normalized-metrics.json',
        'normalized/admin-overhead.json', 'normalized/longitudinal-findings.json')
GATES = ('normalized/validation-report.json',
         'reconciliation/access-extract-reconciliation.json',
         'reconciliation/table45b-reconciliation.json',
         'reconciliation/personnel-compensation-comparison.json')
PROVENANCE = 'reporting/report-provenance.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_analysis(root):
    root = Path(root)
    manifest_bytes = (root / PROVENANCE).read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest.get('gate_status') != 'pass' or not re.fullmatch(r'[0-9a-f]{40}', manifest.get('analysis_ref', '')):
        raise RuntimeError('analysis provenance must identify a passing commit')
    if not str(manifest.get('analysis_run', '')).isdigit():
        raise RuntimeError('analysis provenance must identify a workflow run')
    if not all(manifest.get('source_snapshots', {}).get(k) for k in ('s275', 'normalization')):
        raise RuntimeError('both immutable snapshot tags required')
    inputs = manifest.get('input_sha256', {})
    if not set(DATA + GATES).issubset(inputs):
        raise RuntimeError('incomplete report input provenance')
    evidence = {PROVENANCE: manifest_bytes}
    payload = {}
    for name, expected in inputs.items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or relative.as_posix() != name:
            raise RuntimeError(f'unsafe input path: {name}')
        data = (root / name).read_bytes()
        if digest(data) != expected:
            raise RuntimeError(f'analysis input hash mismatch: {name}')
        evidence[name] = data
        payload[name] = json.loads(data)
    for name in GATES:
        if payload[name].get('status') != 'pass':
            raise RuntimeError(f'comparison requires passing gate: {name}')
    if payload[GATES[0]].get('critical'):
        raise RuntimeError('critical validation findings remain')
    findings = payload[DATA[-1]]
    if findings['source_snapshots'] != manifest['source_snapshots'] or findings['period'] != manifest['period']:
        raise RuntimeError('report/findings provenance mismatch')
    return manifest, payload, evidence


def numeric_leaves(value, prefix=''):
    out = {}
    if isinstance(value, dict):
        for key, item in value.items():
            out.update(numeric_leaves(item, f'{prefix}/{key}'))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value):
            raise RuntimeError(f'nonfinite analytical measure: {prefix}')
        out[prefix] = value
    return out


def rows(payload):
    result = {}
    def add(label, records, category=False):
        for row in records:
            key = (label, row['school_year'], row['job_family'] if category else '')
            if key in result:
                raise RuntimeError(f'duplicate comparison row: {key}')
            result[key] = numeric_leaves(row)
    metrics = payload[DATA[0]]
    add('district', metrics['district'])
    add('category', metrics['categories'], True)
    add('normalized', payload[DATA[1]]['years'])
    add('administration', payload[DATA[2]]['years'])
    return result


def compare(before, after):
    left, right = rows(before), rows(after)
    changes = []
    for key in sorted(set(left) | set(right)):
        a, b = left.get(key, {}), right.get(key, {})
        for measure in sorted(set(a) | set(b)):
            old, new = a.get(measure), b.get(measure)
            if old == new:
                continue
            delta = new-old if old is not None and new is not None else None
            changes.append({'scope': key[0], 'school_year': key[1], 'job_family': key[2] or None,
                            'measure': measure, 'before': old, 'after': new, 'difference': delta,
                            'percent_change': delta/old*100 if delta is not None and old else None,
                            'change_type': 'added' if old is None else 'removed' if new is None else 'changed'})
    return changes


def build(before_root, after_root, output_dir):
    bm, bp, be = load_analysis(before_root)
    am, ap, ae = load_analysis(after_root)
    changes = compare(bp, ap)
    record = {'schema_version': 1, 'status': 'validated_comparison',
              'comparison_code_sha256': digest(Path(__file__).read_bytes()),
              'before': bm, 'after': am, 'changed_measure_count': len(changes), 'changes': changes,
              'evidence_sha256': {f'{label}/{name}': digest(data)
                                 for label, evidence in [('before', be), ('after', ae)]
                                 for name, data in sorted(evidence.items())},
              'limitations': ['Differences include data, normalization, classification, and code changes; this comparison does not attribute causes.',
                             'Personnel compensation is not operating expenditure. Source limitations remain in the retained validation evidence.',
                             'No source or published report is promoted by comparison or revision-record publication.']}
    encoded = (json.dumps(record, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents replacing a previously reviewed evidence bundle.
    with (out/'revision-record.json').open('xb') as handle:
        handle.write(encoded)
    with zipfile.ZipFile(out/'revision-evidence.zip', 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('revision-record.json', encoded)
        for label, evidence in [('before', be), ('after', ae)]:
            for name, data in sorted(evidence.items()):
                archive.writestr(f'{label}/{name}', data)
    summary = {'revision_record_sha256': digest(encoded), 'changed_measure_count': len(changes),
               'before_run': bm['analysis_run'], 'after_run': am['analysis_run']}
    (out/'review-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))
    return record


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--before', required=True)
    p.add_argument('--after', required=True)
    p.add_argument('--output-dir', default='artifacts/revision-review')
    a = p.parse_args(argv)
    build(a.before, a.after, a.output_dir)


if __name__ == '__main__':
    main()
