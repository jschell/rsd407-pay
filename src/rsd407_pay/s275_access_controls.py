from __future__ import annotations
import argparse,csv,json,subprocess
from pathlib import Path
FIELDS=("certfte","clasfte","certbase","clasbase","othersal","tfinsal","cins","cman")
DISTRICT="17407"
def num(v): return float(v or 0)
def derive(db,table,year):
    p=subprocess.run(["mdb-export",str(db),table],check=True,capture_output=True,text=True)
    district=[r for r in csv.DictReader(p.stdout.splitlines()) if r.get("codist","").strip()==DISTRICT]
    if not district: raise RuntimeError(f"{year}: district {DISTRICT} not found")
    rows=[r for r in district if r.get("recno","").strip()=="1"]
    if not rows: raise RuntimeError(f"{year}: no recno=1 personnel rows")
    sums={f:sum(num(r.get(f)) for r in rows) for f in FIELDS}
    return {"school_year":year,"source_rows":len(district),"personnel_rows":len(rows),
      "additional_assignment_rows":len(district)-len(rows),**sums,
      "total_fte":sums["certfte"]+sums["clasfte"],"base_salary":sums["certbase"]+sums["clasbase"],
      "reported_employer_compensation":sums["tfinsal"]+sums["cins"]+sums["cman"]}
def main(argv=None):
    a=argparse.ArgumentParser();a.add_argument("--schema",default="artifacts/reconciliation/s275-access-schema-inventory.json");a.add_argument("--discovery",default="artifacts/reconciliation/s275-access-discovery-report.json");a.add_argument("--output",default="artifacts/reconciliation/s275-access-derived-controls.json");x=a.parse_args(argv)
    d=json.loads(Path(x.schema).read_text()); discovery=json.loads(Path(x.discovery).read_text())
    if discovery["summary"]["years_observed"]!=12 or discovery["summary"]["recno_1_exact_control_matches"]!=12:
        raise RuntimeError("recno=1 personnel-row invariant not established for all 12 years")
    out={"schema_version":2,"district_code":DISTRICT,"derivation_version":"personnel-recno1-v2",
      "personnel_row_rule":"recno=1; empirically reconciled to accepted simplified-extract employee count and FTE in all 12 years",
      "years":[]}
    for r in d["resources"]:
        db=Path("artifacts/reconciliation/raw/s275-access")/r["school_year"]/r["database_file"];table=r["schema"]["tables"][0]
        y=derive(db,table,r["school_year"]);y.update({"table":table,"source_sha256":r["source_sha256"],"database_sha256":r["database_sha256"]});out["years"].append(y)
    Path(x.output).write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
