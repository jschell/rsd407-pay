from __future__ import annotations
import argparse, json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from .sources import discover, fetch, validate_download

def load_config(path): return json.loads(Path(path).read_text())

def collect_one(source, raw_dir:Path):
    source=validate_download(source)
    body,meta=fetch(source.direct_download_url)
    # Re-check bytes written are the bytes represented by the manifest.
    import hashlib
    digest=hashlib.sha256(body).hexdigest()
    if digest != source.sha256: raise RuntimeError(f"{source.school_year}: source changed between validation and write")
    ext=source.file_format
    target=raw_dir/source.school_year/f"s275.{ext}"
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        existing=hashlib.sha256(target.read_bytes()).hexdigest()
        if existing != digest: raise RuntimeError(f"{target} already exists with different content; raw inputs are immutable")
    else: target.write_bytes(body)
    row=asdict(source); row["local_path"]=str(target); row["final_url"]=meta["final_url"]
    return row

def main(argv=None):
    ap=argparse.ArgumentParser(description="Collect immutable OSPI S-275 source files")
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--year"); g.add_argument("--all-final",action="store_true")
    ap.add_argument("--config",default="config/sources.json")
    ap.add_argument("--raw-dir",default="artifacts/raw")
    ap.add_argument("--manifest",default="artifacts/manifests/collection.json")
    args=ap.parse_args(argv)
    config=load_config(args.config); sources=discover(config); by_year={s.school_year:s for s in sources}
    years=config["expected_final_years"] if args.all_final else [args.year]
    unknown=[y for y in years if y not in config["expected_final_years"]]
    if unknown: raise SystemExit("Year is not in expected final-year registry: "+", ".join(unknown))
    missing=[y for y in years if y not in by_year]
    if missing: raise SystemExit("OSPI source not discovered for: "+", ".join(missing))
    rows=[collect_one(by_year[y],Path(args.raw_dir)) for y in years]
    out=Path(args.manifest); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"schema_version":1,"generated_at":datetime.now(timezone.utc).isoformat(),"release_scope":"final","sources":rows},indent=2)+"\n")
    print(f"collected {len(rows)} final S-275 source file(s); manifest: {out}")

if __name__=="__main__": main()
