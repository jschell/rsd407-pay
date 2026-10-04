from __future__ import annotations
import argparse,json
from pathlib import Path
from .cpi import parse
from .enrollment import extract,DISTRICT_CODE,DISTRICT_NAME
from .normalization_snapshot import verify

RAW="artifacts/normalization/raw"

def rebuild():
    manifest=json.loads(Path("artifacts/normalization/normalization-source-manifest.json").read_text())
    verify(manifest)
    windows=[json.loads(Path(RAW+"/bls-cpi-2014-2023.json").read_text()),json.loads(Path(RAW+"/bls-cpi-2024-2025.json").read_text())]
    merged={"status":"REQUEST_SUCCEEDED","Results":{"series":[]}}
    for series_id in ("CUUR0000SA0","CUURS49DSA0"):
        rows=[]
        for payload in windows:
            matches=[x for x in payload["Results"]["series"] if x["seriesID"]==series_id]
            if len(matches)!=1: raise RuntimeError(f"retained BLS response missing {series_id}")
            rows.extend(matches[0]["data"])
        merged["Results"]["series"].append({"seriesID":series_id,"data":rows})
    retained_cpi=json.loads(Path('artifacts/normalization/cpi.json').read_text())
    rebuilt_cpi={"source":retained_cpi["source"],"source_url":retained_cpi["source_url"],"retrieved_at":retained_cpi["retrieved_at"],"raw_source_files":retained_cpi["raw_source_files"],"series":parse(merged)}
    if rebuilt_cpi["series"]!=retained_cpi["series"]: raise RuntimeError("rebuilt CPI does not match retained derived CPI")
    data=Path(RAW+"/p223-final-enrollment.xlsx").read_bytes()
    retained_enrollment=json.loads(Path('artifacts/normalization/enrollment.json').read_text())
    rows=extract(data)
    if rows!=retained_enrollment["years"]: raise RuntimeError("rebuilt enrollment does not match retained derived enrollment")
    print(f"verified retained normalization derivation: {len(rows)} enrollment years and {len(rebuilt_cpi['series'])} CPI series")

def main(argv=None): rebuild()
if __name__=="__main__": main()
