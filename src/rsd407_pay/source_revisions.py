"""Compare current OSPI workbooks with a reviewed immutable source manifest."""
import argparse
import hashlib
import json
import re
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from .sources import discover, fetch
from .workbook import validate_workbook_bytes


def validate_baseline(baseline, expected_years):
    rows = baseline.get('sources', [])
    years = [r.get('school_year') for r in rows]
    if baseline.get('release_scope') != 'final':
        raise ValueError('accepted manifest must identify final scope')
    if sorted(years) != sorted(expected_years) or len(set(years)) != len(years):
        raise ValueError('accepted manifest must contain exact registered year coverage')
    for row in rows:
        if not re.fullmatch(r'[0-9a-f]{64}', row.get('sha256', '')):
            raise ValueError('accepted manifest has missing/invalid source SHA-256')
        if not row.get('direct_download_url'):
            raise ValueError('accepted manifest has missing source URL')
    return {r['school_year']:r for r in rows}


def compare(old, current):
    content = old['sha256'] != current['sha256']
    location = old['direct_download_url'] != current['direct_download_url']
    if content and location:
        return 'content_and_url_revision'
    if content:
        return 'content_revision'
    if location:
        return 'url_relocation'
    return 'unchanged'


def check(baseline, candidates, expected_years, evidence_dir, *, fetcher=fetch,
          validator=validate_workbook_bytes):
    accepted = validate_baseline(baseline, expected_years)
    candidate_list = list(candidates)
    by = {r.school_year:r for r in candidate_list}
    if len(by) != len(candidate_list):
        raise ValueError('duplicate discovered school years')
    rows, errors = [], []
    for year in expected_years:
        old = accepted[year]
        evidence = {'school_year':year,
                    'accepted_source_url':old['direct_download_url'],
                    'accepted_sha256':old['sha256']}
        try:
            if year not in by:
                raise RuntimeError('registered year not discovered on official page')
            source = by[year]
            body, meta = fetcher(source.direct_download_url)
            if len(body)<1024 or b'<html' in body[:1000].lower() or 'text/html' in meta.get('content_type','').lower():
                raise RuntimeError('expected workbook download, received invalid content')
            identity = validator(body, source.file_format)
            observed = asdict(source)
            observed.update(sha256=hashlib.sha256(body).hexdigest(), byte_size=len(body),
                retrieved_at=datetime.now(timezone.utc).isoformat(), http_status=meta.get('status'),
                content_type=meta.get('content_type'), final_url=meta.get('final_url'),
                workbook_identity=identity)
            status = compare(old, observed)
            path = None
            if status in ('content_revision','content_and_url_revision'):
                path = Path(evidence_dir)/year/(observed['sha256']+'.'+source.file_format)
                path.parent.mkdir(parents=True, exist_ok=True)
                # Exclusive creation prevents a monitor rerun overwriting evidence.
                if path.exists():
                    if hashlib.sha256(path.read_bytes()).hexdigest()!=observed['sha256']:
                        raise RuntimeError('existing content-addressed revision evidence is corrupt')
                else:
                    with path.open('xb') as handle:
                        handle.write(body)
            rows.append(dict(evidence, status=status, observed=observed,
                revision_local_path=str(path) if path else None,
                analytical_impact='not_evaluated_requires_rebuild' if status!='unchanged' else 'identical_source_bytes'))
        except Exception as exc:
            # Observe subsequent years even when this year's source cannot be checked.
            errors.append({'school_year':year, 'error':str(exc)})
            rows.append(dict(evidence,status='check_failed',error=str(exc)))
    revisions = [r['school_year'] for r in rows if r['status'] not in ('unchanged','check_failed')]
    return {'schema_version':1, 'status':'fail' if errors else ('review_required' if revisions else 'pass'),
        'accepted_manifest_canonical_json_sha256':hashlib.sha256(json.dumps(baseline,sort_keys=True).encode()).hexdigest(),
        'revision_years':revisions, 'errors':errors, 'years':rows,
        'promotion':'none; accepted sources and published analysis unchanged',
        'limitation':'Byte-level/URL revision detection. Analytical effects require a reviewed rebuild.'}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',default='config/sources.json')
    parser.add_argument('--baseline',default='artifacts/manifests/accepted-collection.json')
    parser.add_argument('--output',default='artifacts/source-revisions.json')
    parser.add_argument('--evidence-dir',default='artifacts/source-revisions')
    a = parser.parse_args(argv)
    config = json.loads(Path(a.config).read_text())
    baseline = json.loads(Path(a.baseline).read_text())
    # This validates accepted coverage before any current-source downloads.
    validate_baseline(baseline,config['expected_final_years'])
    try:
        discovered = discover(config)
        report = check(baseline,discovered,config['expected_final_years'],Path(a.evidence_dir))
    except Exception as exc:
        report = {'schema_version':1,'status':'fail','errors':[{'error':str(exc)}],
                  'promotion':'none; accepted sources and published analysis unchanged'}
    report.update(accepted_snapshot_tag=config['accepted_snapshot_tag'],
        accepted_manifest_file_sha256=hashlib.sha256(Path(a.baseline).read_bytes()).hexdigest(),
        checked_at=datetime.now(timezone.utc).isoformat())
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'revision_years':report.get('revision_years',[]),'errors':report['errors']}))
    if report['status']!='pass':
        raise SystemExit('Source checks require review; see source-revisions.json')

if __name__=='__main__':
    main()
