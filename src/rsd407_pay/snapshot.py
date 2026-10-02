from __future__ import annotations
import argparse, hashlib, json, tarfile
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def build_snapshot(manifest_path, raw_dir, output, tag):
    manifest=json.loads(Path(manifest_path).read_text())
    files=[]
    for source in manifest["sources"]:
        p=Path(source["local_path"])
        digest=sha256(p)
        if digest != source["sha256"]:
            raise RuntimeError(f"hash mismatch before snapshot: {p}")
        files.append({"school_year":source["school_year"],"path":str(p),"sha256":digest})
    meta={"schema_version":1,"snapshot_tag":tag,"collection_manifest":"artifacts/manifests/collection.json","files":files}
    meta_path=Path("artifacts/manifests/source-snapshot.json")
    meta_path.parent.mkdir(parents=True,exist_ok=True)
    meta_path.write_text(json.dumps(meta,indent=2)+"\n")
    with tarfile.open(output,"w:gz") as tf:
        tf.add(manifest_path,arcname="artifacts/manifests/collection.json")
        tf.add(meta_path,arcname="artifacts/manifests/source-snapshot.json")
        for item in files: tf.add(item["path"],arcname=item["path"])
    return meta

def verify_snapshot(root="."):
    root=Path(root)
    meta=json.loads((root/"artifacts/manifests/source-snapshot.json").read_text())
    for item in meta["files"]:
        p=root/item["path"]
        if not p.exists() or sha256(p)!=item["sha256"]:
            raise RuntimeError(f"snapshot verification failed: {item['path']}")
    return meta

def main(argv=None):
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    b=sub.add_parser("build"); b.add_argument("--manifest",default="artifacts/manifests/collection.json"); b.add_argument("--raw-dir",default="artifacts/raw"); b.add_argument("--output",required=True); b.add_argument("--tag",required=True)
    v=sub.add_parser("verify"); v.add_argument("--root",default=".")
    a=ap.parse_args(argv)
    if a.cmd=="build":
        m=build_snapshot(a.manifest,a.raw_dir,a.output,a.tag); print(f"built {m['snapshot_tag']} with {len(m['files'])} files")
    else:
        m=verify_snapshot(a.root); print(f"verified {m['snapshot_tag']} with {len(m['files'])} files")
if __name__=="__main__": main()
