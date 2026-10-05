from __future__ import annotations
import argparse,json
from pathlib import Path
MONEY=("base_salary","total_salary","insurance","mandatory_benefits","reported_employer_compensation")
def verify(derived,accepted):
    errors=[]
    if derived.get("district_code")!=accepted.get("district_code"): errors.append("district code differs")
    got={x["school_year"]:x for x in derived["years"]}; exp={x["school_year"]:x for x in accepted["years"]}
    if set(got)!=set(exp): errors.append(f"year coverage differs: derived={sorted(got)} accepted={sorted(exp)}")
    for year in sorted(set(got)&set(exp)):
        g,e=got[year],exp[year]
        if g["personnel_rows"]!=e["personnel_rows"]: errors.append(f"{year}: personnel_rows {g['personnel_rows']} != {e['personnel_rows']}")
        if abs(g["total_fte"]-e["total_fte"])>1e-6: errors.append(f"{year}: total_fte drift {g['total_fte']} != {e['total_fte']}")
        for k in MONEY:
            if g[k]!=e[k]: errors.append(f"{year}: {k} drift {g[k]} != {e[k]}")
        for k in ("source_sha256","database_sha256","table"):
            if g[k]!=e[k]: errors.append(f"{year}: provenance {k} differs")
    return errors
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument("--derived",default="artifacts/reconciliation/s275-access-derived-controls.json");p.add_argument("--accepted",default="controls/s275-access-riverview.json");a=p.parse_args(argv)
    errors=verify(json.loads(Path(a.derived).read_text()),json.loads(Path(a.accepted).read_text()))
    report={"status":"fail" if errors else "pass","errors":errors};print(json.dumps(report,indent=2))
    if errors: raise SystemExit(1)
if __name__=="__main__":main()
