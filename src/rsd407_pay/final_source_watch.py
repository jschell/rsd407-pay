"""Surface explicitly final personnel-workbook links outside accepted coverage."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from .sources import Links, fetch, normalize_year, s275_section

def candidates(html, config, page_url=None):
    parser = Links()
    parser.feed(s275_section(html))
    found = {}
    for href, text in parser.links:
        url = urljoin(page_url or config['landing_page'], href)
        path = urlparse(url).path
        label = (text+' '+path).lower()
        words = re.sub(r'[_/.-]+', ' ', label)
        year = normalize_year(label)
        if urlparse(url).hostname not in config['allowed_hosts']:
            continue
        if Path(path).suffix.lower() not in ('.xlsx', '.xls'):
            continue
        if not year or int(year[-2:]) != (int(year[:4])+1)%100:
            continue
        if not any(term in label for term in ('personnel','s-275','s275')):
            continue
        if not re.search(r'\bfinal\b', words) or re.search(r'\b(preliminary|draft)\b', words):
            continue
        found[(year,url)] = {'school_year': year, 'source_url': url,
            'source_label': text, 'finality_evidence': 'Explicit final marker in official link label/path',
            'outside_accepted_years': year not in config['expected_final_years'],
            'status': 'candidate_requires_validation'}
    return [found[k] for k in sorted(found)]

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config/sources.json')
    parser.add_argument('--html', help='Use saved official-page HTML for reproducible/offline discovery')
    parser.add_argument('--output', default='artifacts/final-source-watch.json')
    parser.add_argument('--page-output', default='artifacts/s275-source-page.html')
    a = parser.parse_args(argv)
    config = json.loads(Path(a.config).read_text())
    if a.html:
        body = Path(a.html).read_bytes(); page_url = config['landing_page']
    else:
        body, metadata = fetch(config['landing_page']); page_url = metadata['final_url']
    page_file = Path(a.page_output); page_file.parent.mkdir(parents=True, exist_ok=True)
    page_file.write_bytes(body)
    rows = candidates(body.decode('utf-8', 'replace'), config, page_url)
    report = {'schema_version': 1, 'checked_at': datetime.now(timezone.utc).isoformat(),
        'source_page_url': page_url, 'source_page_sha256': hashlib.sha256(body).hexdigest(),
        'accepted_years': config['expected_final_years'], 'candidates': rows,
        'new_final_year_candidates': sorted({r['school_year'] for r in rows if r['outside_accepted_years']}),
        'limitation': 'Link discovery only. Does not verify workbook contents, compare historical file hashes, or promote a year. No candidates does not prove that no newer final data exist.'}
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__=='__main__':
    main()
