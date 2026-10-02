from __future__ import annotations
import argparse,csv,json
from collections import defaultdict
from pathlib import Path

NUMERIC=("certificated_fte","classified_fte","base_salary","total_salary","insurance_benefits","mandatory_benefits")

def n(row,key):
    try: return float(row.get(key) or 0)
    except (TypeError,ValueError): return 0.0

def aggregate(rows):
    groups=defaultdict(list)
    years=defaultdict(list)
    for row in rows:
        groups[(row["school_year"],row["job_family"])].append(row)
        years[row["school_year"]].append(row)

    def summarize(items):
        sums={k:sum(n(r,k) for r in items) for k in NUMERIC}
        total_fte=sums["certificated_fte"]+sums["classified_fte"]
        return {
            "employee_rows":len(items),
            **sums,
            "total_fte":total_fte,
            "base_salary_per_fte":sums["base_salary"]/total_fte if total_fte else None,
            "total_salary_per_fte":sums["total_salary"]/total_fte if total_fte else None,
            "reported_employer_compensation":sums["total_salary"]+sums["insurance_benefits"]+sums["mandatory_benefits"],
            "zero_fte_rows":sum(1 for r in items if n(r,"certificated_fte")+n(r,"classified_fte")==0),
            "total_salary_below_base_rows":sum(1 for r in items if n(r,"total_salary") < n(r,"base_salary")),
        }

    district={y:summarize(items) for y,items in sorted(years.items())}
    categories=[]
    for (year,family),items in sorted(groups.items()):
        x=summarize(items); d=district[year]
        x.update({
            "school_year":year,"job_family":family,
            "share_district_fte":x["total_fte"]/d["total_fte"] if d["total_fte"] else None,
            "share_district_base_salary":x["base_salary"]/d["base_salary"] if d["base_salary"] else None,
            "share_district_total_salary":x["total_salary"]/d["total_salary"] if d["total_salary"] else None,
        })
        categories.append(x)
    return {"schema_version":1,"district":[{"school_year":y,**x} for y,x in district.items()],"categories":categories}

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default="artifacts/normalized/rsd407-job-family.csv")
    ap.add_argument("--output",default="artifacts/normalized/annual-metrics.json")
    a=ap.parse_args()
    with Path(a.input).open(newline="",encoding="utf-8") as h: rows=list(csv.DictReader(h))
    report=aggregate(rows)
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n")
    print(f"wrote metrics for {len(report['district'])} school years and {len(report['categories'])} year/family groups")
if __name__=="__main__": main()
