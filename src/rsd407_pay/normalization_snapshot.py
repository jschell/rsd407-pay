from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

FILES=[
 "artifacts/normalization/raw/bls-cpi-2014-2023.json",
 "artifacts/normalization/raw/bls-cpi-2024-2025.json",
 "artifacts/normalization/raw/p223-final-enrollment.xlsx",
 "artifacts/normalization/cpi.json",
 "artifacts/normalization/enrollment.json",
 "artifacts/normalization/p223-inventory.json",
]
def sha256(path):
 h=hashlib.sha256()
 with Path(path).open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
def build(tag=None):
 items=[]
 for name in FILES:
  p=Path(name)
  if not p.exists(): raise RuntimeError(f"normalization source file missing: {name}")
  items.append({"path":name,"sha256":sha256(p),"size_bytes":p.stat().st_size})
 return {"schema_version":1,"snapshot_tag":tag,"files":items}
def verify(manifest):
 for item in manifest["files"]:
  p=Path(item["path"])
  if not p.exists() or sha256(p)!=item["sha256"]: raise RuntimeError(f"normalization snapshot verification failed: {item['path']}")
 return manifest
def main(argv=None):
 p=argparse.ArgumentParser(); p.add_argument("--output",default="artifacts/normalization/normalization-source-manifest.json"); p.add_argument("--tag"); p.add_argument("--verify",action="store_true"); a=p.parse_args(argv)
 path=Path(a.output)
 if a.verify:
  m=verify(json.loads(path.read_text())); print(f"verified {len(m['files'])} normalization source files")
 else:
  m=build(a.tag); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(m,indent=2)+"\n"); print(f"manifested {len(m['files'])} normalization source files")
if __name__=="__main__": main()
