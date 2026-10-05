from __future__ import annotations
import argparse,hashlib,json,subprocess,urllib.request,zipfile
from pathlib import Path
UA="rsd407-pay/1.0"
def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def download(url,path):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=120) as r, path.open("wb") as w:
        while True:
            b=r.read(1024*1024)
            if not b: break
            w.write(b)
def access_files(path,outdir):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            names=[n for n in z.namelist() if n.lower().endswith((".mdb",".accdb"))]
            if len(names)!=1: raise RuntimeError(f"expected one Access database in {path.name}, found {names}")
            z.extract(names[0],outdir); return outdir/names[0]
    if path.suffix.lower() in (".mdb",".accdb"): return path
    raise RuntimeError(f"unsupported Access source container: {path}")
def schema(db):
    tables=[x.strip() for x in subprocess.run(
        ["mdb-tables","-1",str(db)],check=True,capture_output=True,text=True
    ).stdout.splitlines() if x.strip()]
    schema_sql=subprocess.run(
        ["mdb-schema",str(db)],check=True,capture_output=True,text=True
    ).stdout
    return {"tables":tables,"schema_sql":schema_sql}
def build(inventory,root):
    resources=[]
    for item in inventory["resources"]:
        year=item["school_year"]; d=root/year; d.mkdir(parents=True,exist_ok=True)
        source=d/"source"; download(item["url"],source); db=access_files(source,d)
        resources.append({"school_year":year,"url":item["url"],"source_sha256":sha256(source),"source_bytes":source.stat().st_size,
                          "database_file":db.name,"database_sha256":sha256(db),"schema":schema(db)})
    return {"schema_version":1,"source_class":"s275_access","resources":resources}
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--inventory",default="artifacts/reconciliation/s275-access-source-inventory.json"); p.add_argument("--raw-dir",default="artifacts/reconciliation/raw/s275-access"); p.add_argument("--output",default="artifacts/reconciliation/s275-access-schema-inventory.json"); a=p.parse_args(argv)
    report=build(json.loads(Path(a.inventory).read_text()),Path(a.raw_dir)); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n"); print(f"Inventoried {len(report['resources'])} Access databases")
if __name__=="__main__": main()
