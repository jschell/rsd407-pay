from __future__ import annotations
import argparse,json
from pathlib import Path
from .cpi import parse, merge_windows
from .enrollment import extract,DISTRICT_CODE,DISTRICT_NAME
from .normalization_snapshot import verify

RAW="artifacts/normalization/raw"

def rebuild():
    manifest=json.loads(Path("artifacts/normalization/normalization-source-manifest.json").read_text())
    verify(manifest)
    retained_cpi=json.loads(Path('artifacts/normalization/cpi.json').read_text())
    paths = retained_cpi['raw_source_files']
    if not paths or len(paths) != len(set(paths)):
        raise RuntimeError("retained CPI raw paths must be nonempty and unique")
    verified = {item['path'] for item in manifest['files']}
    if any(path not in verified or not Path(path).name.startswith('bls-cpi-') for path in paths):
        raise RuntimeError("CPI raw input is outside verified normalization manifest")
    windows = [json.loads(Path(path).read_text()) for path in paths]
    merged = merge_windows(windows)
    rebuilt_cpi={"source":retained_cpi["source"],"source_url":retained_cpi["source_url"],"retrieved_at":retained_cpi["retrieved_at"],"raw_source_files":retained_cpi["raw_source_files"],"series":parse(merged)}
    if rebuilt_cpi["series"]!=retained_cpi["series"]: raise RuntimeError("rebuilt CPI does not match retained derived CPI")
    data=Path(RAW+"/p223-final-enrollment.xlsx").read_bytes()
    retained_enrollment=json.loads(Path('artifacts/normalization/enrollment.json').read_text())
    rows=extract(data)
    if rows!=retained_enrollment["years"]: raise RuntimeError("rebuilt enrollment does not match retained derived enrollment")
    print(f"verified retained normalization derivation: {len(rows)} enrollment years and {len(rebuilt_cpi['series'])} CPI series")

def main(argv=None): rebuild()
if __name__=="__main__": main()

