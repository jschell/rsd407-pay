from __future__ import annotations
import argparse, hashlib, json, urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER_AGENT = "rsd407-pay/1.0"
DISTRICT_CODE = "17407"

def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as response: return response.read()

def collect(inventory: dict, raw_dir: Path) -> dict:
    raw_dir.mkdir(parents=True, exist_ok=True); resources=[]
    for r in inventory.get("resources", []):
        data=fetch_bytes(r["url"])
        if not data.startswith(b"%PDF"): raise RuntimeError(f"{r['school_year']}: source is not a PDF")
        path=raw_dir/f"personnel-summary-{r['school_year']}.pdf"; path.write_bytes(data)
        resources.append({**r,"local_file":str(path),"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"retrieved_at":datetime.now(timezone.utc).isoformat()})
    return {"schema_version":1,"district_code":DISTRICT_CODE,"resources":resources}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--inventory",default="artifacts/reconciliation/table47-control-inventory.json"); p.add_argument("--raw-dir",default="artifacts/reconciliation/raw"); p.add_argument("--output",default="artifacts/reconciliation/table47-source-manifest.json"); a=p.parse_args(argv)
    report=collect(json.loads(Path(a.inventory).read_text()),Path(a.raw_dir)); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    print(f"Retained {len(report['resources'])} official Personnel Summary PDFs")
if __name__=="__main__": main()
