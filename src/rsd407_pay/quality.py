from __future__ import annotations
import argparse,csv,json
from collections import defaultdict
from pathlib import Path
from .metrics import n

def build_quality_report(rows):
    groups=defaultdict(list)
    for row in rows: groups[(row["school_year"],row["job_family"])].append(row)
    detail=[]
    for (year,family),items in sorted(groups.items()):
        zero=sum(1 for r in items if n(r,"certificated_fte")+n(r,"classified_fte")==0)
        below=sum(1 for r in items if n(r,"total_salary") < n(r,"base_salary"))
        if zero or below:
            detail.append({"school_year":year,"job_family":family,"employee_rows":len(items),
                           "zero_fte_rows":zero,"total_salary_below_base_rows":below})
    annual=[]
    years=sorted({r["school_year"] for r in rows})
    for year in years:
        items=[r for r in rows if r["school_year"]==year]
        annual.append({"school_year":year,"employee_rows":len(items),
            "zero_fte_rows":sum(1 for r in items if n(r,"certificated_fte")+n(r,"classified_fte")==0),
            "total_salary_below_base_rows":sum(1 for r in items if n(r,"total_salary") < n(r,"base_salary"))})
    return {"schema_version":1,
      "interpretation":{"zero_fte_rows":"Source employee-year rows with certificated FTE + classified FTE = 0; preserved, not repaired.",
        "total_salary_below_base_rows":"Source employee-year rows where reported total salary is less than reported base salary; preserved, not repaired.",
        "warning":"Counts are source-quality diagnostics, not evidence of payroll error or employee assignment count."},
      "annual":annual,"by_job_family":detail}

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--input",default="artifacts/normalized/rsd407-job-family.csv"); ap.add_argument("--output",default="artifacts/normalized/data-quality.json")
    a=ap.parse_args()
    with Path(a.input).open(newline="",encoding="utf-8") as h: rows=list(csv.DictReader(h))
    report=build_quality_report(rows); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    print("data-quality conditions by year/job family:")
    for x in report["by_job_family"]:
        print(f"{x['school_year']} | {x['job_family']} | rows={x['employee_rows']} zero_fte={x['zero_fte_rows']} total_salary_below_base={x['total_salary_below_base_rows']}")
if __name__=="__main__": main()
