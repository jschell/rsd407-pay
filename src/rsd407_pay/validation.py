from __future__ import annotations
import argparse,csv,json
from collections import Counter
from pathlib import Path
from .metrics import NUMERIC

YEARS=[f"{y}-{str(y+1)[-2:]}" for y in range(2013,2025)]
CRITICAL_NUMERIC=("certificated_fte","classified_fte","base_salary","total_salary","insurance_benefits","mandatory_benefits")

def number(row,key):
    try: return float(row.get(key) or 0)
    except (TypeError,ValueError): return None

def validate(rows,metrics):
    critical=[]; warnings=[]
    years=sorted({r["school_year"] for r in rows})
    if years != YEARS:
        critical.append({"check":"year_coverage","detail":f"expected {YEARS}, got {years}"})
    keys=[(r.get("school_year"),r.get("source_sha256"),r.get("source_sheet"),r.get("source_row")) for r in rows]
    duplicates=[k for k,n in Counter(keys).items() if n>1]
    if duplicates:
        critical.append({"check":"duplicate_source_rows","count":len(duplicates)})
    for key in CRITICAL_NUMERIC:
        bad=sum(1 for r in rows if number(r,key) is None)
        neg=sum(1 for r in rows if number(r,key) is not None and number(r,key)<0)
        if bad: critical.append({"check":"non_numeric","field":key,"count":bad})
        if neg: critical.append({"check":"negative_value","field":key,"count":neg})
    zero=sum(1 for r in rows if (number(r,"certificated_fte") or 0)+(number(r,"classified_fte") or 0)==0)
    below=sum(1 for r in rows if (number(r,"total_salary") or 0)<(number(r,"base_salary") or 0))
    if zero: warnings.append({"check":"zero_fte_rows","count":zero})
    if below: warnings.append({"check":"total_salary_below_base","count":below})
    district=metrics.get("district",[])
    if [x["school_year"] for x in district] != YEARS:
        critical.append({"check":"metrics_year_coverage","detail":"annual metrics do not contain exact expected years"})
    discontinuities=[]
    for previous,current in zip(district,district[1:]):
        for field in ("employee_rows","total_fte","base_salary","total_salary","reported_employer_compensation"):
            a,b=float(previous[field]),float(current[field])
            pct=(b/a-1) if a else None
            if pct is not None and abs(pct)>=0.15:
                discontinuities.append({"from":previous["school_year"],"to":current["school_year"],"field":field,"percent_change":pct})
    if discontinuities:
        warnings.append({"check":"large_year_over_year_changes","threshold":0.15,"items":discontinuities})
    return {"schema_version":1,"status":"fail" if critical else "pass","critical":critical,"warnings":warnings,
            "external_reconciliation":{"status":"pending","note":"Independent OSPI personnel-summary reconciliation is required before Plan 07 completion."}}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--input",default="artifacts/normalized/rsd407-job-family.csv"); p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json"); p.add_argument("--output",default="artifacts/normalized/validation-report.json"); a=p.parse_args(argv)
    with Path(a.input).open(newline="",encoding="utf-8") as h: rows=list(csv.DictReader(h))
    report=validate(rows,json.loads(Path(a.metrics).read_text()))
    Path(a.output).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if report["status"]!="pass": raise SystemExit("critical validation checks failed")
if __name__=="__main__": main()
