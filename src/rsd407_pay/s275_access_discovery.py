from __future__ import annotations
import argparse,csv,json,subprocess,traceback
from pathlib import Path
DISTRICT="17407"
FIELDS=("certfte","clasfte","certbase","clasbase","othersal","tfinsal","cins","cman")
EXPECTED={
"2013-14":(373,294.471),"2014-15":(386,300.858),"2015-16":(413,313.194),
"2016-17":(419,320.303),"2017-18":(424,328.361),"2018-19":(430,333.136),
"2019-20":(442,342.184),"2020-21":(432,330.982),"2021-22":(433,340.612),
"2022-23":(421,322.603),"2023-24":(404,322.499),"2024-25":(442,337.367)}
def num(v):
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0
def totals(rows):
    return {"rows":len(rows),"total_fte":sum(num(r.get("certfte"))+num(r.get("clasfte")) for r in rows),
      "base_salary":sum(num(r.get("certbase"))+num(r.get("clasbase")) for r in rows),
      "total_salary":sum(num(r.get("tfinsal")) for r in rows),
      "insurance":sum(num(r.get("cins")) for r in rows),
      "mandatory_benefits":sum(num(r.get("cman")) for r in rows)}
def inspect_year(db,table,year):
    p=subprocess.run(["mdb-export",str(db),table],check=True,capture_output=True,text=True)
    rows=[r for r in csv.DictReader(p.stdout.splitlines()) if r.get("codist","").strip()==DISTRICT]
    if not rows: raise RuntimeError("district not found")
    seq={}
    for r in rows: seq.setdefault(r.get("recno","").strip(),[]).append(r)
    first=seq.get("1",[])
    expected_rows,expected_fte=EXPECTED[year]
    all_t,first_t=totals(rows),totals(first)
    return {"status":"observed","school_year":year,"table":table,
      "all_rows":all_t,"recno_1":first_t,
      "recno_values":{k:len(v) for k,v in sorted(seq.items())},
      "known_simplified_control":{"employee_rows":expected_rows,"total_fte":expected_fte},
      "recno_1_comparison":{"row_difference":first_t["rows"]-expected_rows,
        "fte_difference":first_t["total_fte"]-expected_fte}}
def run(schema):
    out={"schema_version":1,"district_code":DISTRICT,"mode":"fail-complete-discovery","years":[],"summary":{}}
    for r in schema["resources"]:
        year=r["school_year"]
        try:
            db=Path("artifacts/reconciliation/raw/s275-access")/year/r["database_file"]
            item=inspect_year(db,r["schema"]["tables"][0],year)
        except Exception as e:
            item={"status":"error","school_year":year,"error_type":type(e).__name__,"error":str(e)}
        out["years"].append(item)
    errors=[y for y in out["years"] if y["status"]=="error"]
    matches=[y for y in out["years"] if y["status"]=="observed" and y["recno_1_comparison"]["row_difference"]==0 and abs(y["recno_1_comparison"]["fte_difference"])<1e-6]
    out["summary"]={"years_attempted":len(out["years"]),"years_observed":len(out["years"])-len(errors),
      "years_error":len(errors),"recno_1_exact_control_matches":len(matches)}
    return out
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument("--schema",default="artifacts/reconciliation/s275-access-schema-inventory.json");p.add_argument("--output",default="artifacts/reconciliation/s275-access-discovery-report.json");a=p.parse_args(argv)
    out=run(json.loads(Path(a.schema).read_text()));Path(a.output).write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
