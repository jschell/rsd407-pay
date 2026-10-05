from __future__ import annotations
import argparse,csv,json,subprocess
from pathlib import Path
FIELDS=("certfte","clasfte","certbase","clasbase","othersal","tfinsal","cins","cman")
DISTRICT="17407"
def num(v): return float(v or 0)
def derive(db,table,year):
    p=subprocess.run(["mdb-export",str(db),table],check=True,capture_output=True,text=True)
    rows=[r for r in csv.DictReader(p.stdout.splitlines()) if r.get("codist","").strip()==DISTRICT]
    if not rows: raise RuntimeError(f"{year}: district {DISTRICT} not found")
    people={}
    for r in rows:
        key=r.get("recno","").strip()
        if not key: raise RuntimeError(f"{year}: blank recno")
        vals=tuple(r.get(f,"").strip() for f in FIELDS)
        if key in people and people[key]!=vals: raise RuntimeError(f"{year}: personnel fields vary within recno {key}")
        people[key]=vals
    sums={f:sum(num(v[i]) for v in people.values()) for i,f in enumerate(FIELDS)}
    return {"school_year":year,"source_rows":len(rows),"unique_personnel":len(people),"assignment_duplicate_rows":len(rows)-len(people),**sums,
      "total_fte":sums["certfte"]+sums["clasfte"],"base_salary":sums["certbase"]+sums["clasbase"],
      "reported_employer_compensation":sums["tfinsal"]+sums["cins"]+sums["cman"]}
def main(argv=None):
    a=argparse.ArgumentParser(); a.add_argument("--schema",default="artifacts/reconciliation/s275-access-schema-inventory.json"); a.add_argument("--output",default="artifacts/reconciliation/s275-access-derived-controls.json"); x=a.parse_args(argv)
    d=json.loads(Path(x.schema).read_text()); out={"schema_version":1,"district_code":DISTRICT,"derivation_version":"personnel-recno-v1","years":[]}
    for r in d["resources"]:
        db=Path("artifacts/reconciliation/raw/s275-access")/r["school_year"]/r["database_file"]
        table=r["schema"]["tables"][0]
        y=derive(db,table,r["school_year"]); y.update({"table":table,"source_sha256":r["source_sha256"],"database_sha256":r["database_sha256"]}); out["years"].append(y)
    Path(x.output).write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2))
if __name__=="__main__": main()
