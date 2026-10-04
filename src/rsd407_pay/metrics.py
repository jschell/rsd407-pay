from __future__ import annotations
import argparse,csv,json,math
from collections import defaultdict
from pathlib import Path

NUMERIC=("certificated_fte","classified_fte","base_salary","total_salary","insurance_benefits","mandatory_benefits")
RECONCILE=("employee_rows",*NUMERIC,"total_fte","reported_employer_compensation","zero_fte_rows","total_salary_below_base_rows")
CHANGE=("employee_rows","total_fte","base_salary","total_salary","reported_employer_compensation","base_salary_per_fte","total_salary_per_fte")

def n(row,key):
    try: return float(row.get(key) or 0)
    except (TypeError,ValueError): return 0.0

def _delta(current,reference):
    if current is None or reference is None: return {"absolute":None,"percent":None}
    return {"absolute":current-reference,"percent":((current/reference)-1) if reference else None}

def _changes(records):
    baseline=records[0] if records else None
    previous=None
    out=[]
    for record in records:
        item=dict(record)
        item["change"]={k:{"year_over_year":_delta(record.get(k),previous.get(k) if previous else None),
                           "from_baseline":_delta(record.get(k),baseline.get(k) if baseline else None)}
                        for k in CHANGE}
        out.append(item); previous=record
    return out

def validate_reconciliation(district,categories,tol=1e-6):
    by_year=defaultdict(list)
    for row in categories: by_year[row["school_year"]].append(row)
    for d in district:
        cats=by_year[d["school_year"]]
        for key in RECONCILE:
            actual=sum(x[key] for x in cats)
            expected=d[key]
            if not math.isclose(actual,expected,rel_tol=tol,abs_tol=tol):
                raise RuntimeError(f"category reconciliation failed for {d['school_year']} {key}: {actual} != {expected}")

def aggregate(rows):
    groups=defaultdict(list); years=defaultdict(list)
    for row in rows:
        groups[(row["school_year"],row["job_family"])].append(row); years[row["school_year"]].append(row)

    def summarize(items):
        sums={k:sum(n(r,k) for r in items) for k in NUMERIC}
        total_fte=sums["certificated_fte"]+sums["classified_fte"]
        return {"employee_rows":len(items),**sums,"total_fte":total_fte,
            "base_salary_per_fte":sums["base_salary"]/total_fte if total_fte else None,
            "total_salary_per_fte":sums["total_salary"]/total_fte if total_fte else None,
            "reported_employer_compensation":sums["total_salary"]+sums["insurance_benefits"]+sums["mandatory_benefits"],
            "zero_fte_rows":sum(1 for r in items if n(r,"certificated_fte")+n(r,"classified_fte")==0),
            "total_salary_below_base_rows":sum(1 for r in items if n(r,"total_salary") < n(r,"base_salary"))}

    district=[{"school_year":y,**summarize(items)} for y,items in sorted(years.items())]
    district_by_year={x["school_year"]:x for x in district}
    categories=[]
    for (year,family),items in sorted(groups.items()):
        x=summarize(items); d=district_by_year[year]
        x.update({"school_year":year,"job_family":family,
            "share_district_fte":x["total_fte"]/d["total_fte"] if d["total_fte"] else None,
            "share_district_base_salary":x["base_salary"]/d["base_salary"] if d["base_salary"] else None,
            "share_district_total_salary":x["total_salary"]/d["total_salary"] if d["total_salary"] else None})
        categories.append(x)
    validate_reconciliation(district,categories)
    district=_changes(district)
    family_groups=defaultdict(list)
    for x in categories: family_groups[x["job_family"]].append(x)
    categories=[x for family in sorted(family_groups) for x in _changes(family_groups[family])]
    return {"schema_version":2,"baseline_school_year":district[0]["school_year"] if district else None,"district":district,"categories":categories}

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--input",default="artifacts/normalized/rsd407-job-family.csv"); ap.add_argument("--output",default="artifacts/normalized/annual-metrics.json")
    a=ap.parse_args()
    with Path(a.input).open(newline="",encoding="utf-8") as h: rows=list(csv.DictReader(h))
    report=aggregate(rows)
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    print(f"wrote metrics for {len(report['district'])} school years and {len(report['categories'])} year/family groups; baseline={report['baseline_school_year']}")
    for d in report["district"]:
        print(f"{d['school_year']}: rows={d['employee_rows']} fte={d['total_fte']:.3f} zero_fte={d['zero_fte_rows']} total_salary_below_base={d['total_salary_below_base_rows']}")
    print("category reconciliation: PASS")
if __name__=="__main__": main()
