from __future__ import annotations
import argparse,csv,json,subprocess
from pathlib import Path
DISTRICT="17407"
def num(v): return float(v or 0)
def inspect(db,table,year):
    p=subprocess.run(["mdb-export",str(db),table],check=True,capture_output=True,text=True)
    rows=[r for r in csv.DictReader(p.stdout.splitlines()) if r.get("codist","").strip()==DISTRICT]
    seq={}
    for r in rows:
        k=r.get("recno","").strip()
        g=seq.setdefault(k,{"rows":0,"total_fte":0.0,"base_salary":0.0,"total_salary":0.0})
        g["rows"]+=1
        g["total_fte"]+=num(r.get("certfte"))+num(r.get("clasfte"))
        g["base_salary"]+=num(r.get("certbase"))+num(r.get("clasbase"))
        g["total_salary"]+=num(r.get("tfinsal"))
    return {"school_year":year,"source_rows":len(rows),"recno":seq}
def main(argv=None):
    a=argparse.ArgumentParser(); a.add_argument("--schema",default="artifacts/reconciliation/s275-access-schema-inventory.json"); a.add_argument("--output",default="artifacts/reconciliation/s275-access-recno-diagnostic.json"); x=a.parse_args(argv)
    d=json.loads(Path(x.schema).read_text()); out={"schema_version":1,"district_code":DISTRICT,"years":[]}
    for r in d["resources"]:
        db=Path("artifacts/reconciliation/raw/s275-access")/r["school_year"]/r["database_file"]; table=r["schema"]["tables"][0]
        out["years"].append(inspect(db,table,r["school_year"]))
    Path(x.output).write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2))
if __name__=="__main__": main()
