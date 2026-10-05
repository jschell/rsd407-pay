from __future__ import annotations
import argparse,csv,json,subprocess
from pathlib import Path
DISTRICT="17407"
TERMS=("fte","salary","benefit","insurance","mandatory","district","cert","class","assignment","duty")
def fields(db,table):
    p=subprocess.run(["mdb-export",str(db),table],check=True,capture_output=True,text=True)
    return next(csv.reader([p.stdout.splitlines()[0]]))
def relevant(names):
    return [n for n in names if any(t in n.lower() for t in TERMS)]
def inspect(report):
    out={"schema_version":1,"district_code":DISTRICT,"years":[]}
    for r in report["resources"]:
        db=Path("artifacts/reconciliation/raw/s275-access")/r["school_year"]/r["database_file"]
        tables=r["schema"]["tables"]
        rows=[]
        for table in tables:
            try: cols=fields(db,table)
            except (subprocess.CalledProcessError,StopIteration): continue
            rel=relevant(cols)
            if rel: rows.append({"table":table,"columns":cols,"relevant_columns":rel})
        if not rows:
            raise RuntimeError(f"{r['school_year']}: no candidate control fields found; header/schema inspection is invalid")
        out["years"].append({"school_year":r["school_year"],"source_sha256":r["source_sha256"],"database_sha256":r["database_sha256"],"candidate_tables":rows})
    return out
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--schema",default="artifacts/reconciliation/s275-access-schema-inventory.json"); p.add_argument("--output",default="artifacts/reconciliation/s275-access-control-candidates.json"); a=p.parse_args(argv)
    report=inspect(json.loads(Path(a.schema).read_text())); Path(a.output).write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
