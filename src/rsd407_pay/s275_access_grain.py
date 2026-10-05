from __future__ import annotations
import argparse,csv,json,subprocess
from pathlib import Path
DISTRICT="17407"
PERSONNEL_FIELDS=("certfte","clasfte","certbase","clasbase","othersal","tfinsal","cins","cman")
CANDIDATES=(
 ("recno",),
 ("recno","cert"),
 ("recno","lname","fname","mname"),
 ("cert",),
 ("lname","fname","mname"),
 ("lname","fname","mname","suffix"),
)
def inspect(db,table,year):
    p=subprocess.run(["mdb-export",str(db),table],check=True,capture_output=True,text=True)
    rows=[r for r in csv.DictReader(p.stdout.splitlines()) if r.get("codist","").strip()==DISTRICT]
    out={"school_year":year,"source_rows":len(rows),"candidates":[]}
    for fields in CANDIDATES:
        if not all(f in rows[0] for f in fields): continue
        groups={}
        for r in rows:
            key=tuple(r.get(f,"").strip() for f in fields)
            vals=tuple(r.get(f,"").strip() for f in PERSONNEL_FIELDS)
            g=groups.setdefault(key,set()); g.add(vals)
        conflicts=sum(1 for v in groups.values() if len(v)>1)
        blank_keys=sum(1 for k in groups if not any(k))
        out["candidates"].append({"fields":list(fields),"unique_keys":len(groups),"conflicting_keys":conflicts,"blank_keys":blank_keys,"duplicate_rows":len(rows)-len(groups)})
    return out
def main(argv=None):
    a=argparse.ArgumentParser(); a.add_argument("--schema",default="artifacts/reconciliation/s275-access-schema-inventory.json"); a.add_argument("--output",default="artifacts/reconciliation/s275-access-grain-diagnostic.json"); x=a.parse_args(argv)
    d=json.loads(Path(x.schema).read_text()); out={"schema_version":1,"district_code":DISTRICT,"years":[]}
    for r in d["resources"]:
        db=Path("artifacts/reconciliation/raw/s275-access")/r["school_year"]/r["database_file"]; table=r["schema"]["tables"][0]
        out["years"].append(inspect(db,table,r["school_year"]))
    Path(x.output).write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2))
if __name__=="__main__": main()
