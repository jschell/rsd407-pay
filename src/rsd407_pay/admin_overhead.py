from __future__ import annotations
import argparse,json
from pathlib import Path
from .normalize_metrics import YEARS,CPI

STRICT={"district/central administration"}
SCHOOL={"principals/APs"}
AMBIGUOUS={"other classified"}

def build(metrics,enrollment,cpi):
    district={x["school_year"]:x for x in metrics["district"]}
    categories={(x["school_year"],x["job_family"]):x for x in metrics["categories"]}
    enroll={x["school_year"]:x for x in enrollment["years"]}
    series=cpi["series"]
    out=[]
    for sy in YEARS:
        d=district[sy]; students=float(enroll[sy]["student_fte"])
        central=categories.get((sy,"district/central administration"))
        school=categories.get((sy,"principals/APs"))
        if central is None or school is None: raise RuntimeError(f"{sy} missing required administration category")
        def group(rows):
            fte=sum(float(x["total_fte"]) for x in rows)
            comp=sum(float(x["reported_employer_compensation"]) for x in rows)
            salary=sum(float(x["total_salary"]) for x in rows)
            return {"fte":fte,"total_salary":salary,"reported_employer_compensation":comp,
                    "fte_per_1000_student_fte":fte/students*1000,
                    "total_salary_per_student_fte":salary/students,
                    "employer_compensation_per_student_fte":comp/students,
                    "share_district_employer_compensation":comp/float(d["reported_employer_compensation"])}
        strict=group([central]); school_g=group([school]); combined=group([central,school])
        end=int("20"+sy[-2:])
        for g in (strict,school_g,combined):
            g["constant_2025_dollars"]={}
            for name in CPI:
                vals=series[name]["values"]; factor=float(vals["2025"])/float(vals[str(end)])
                g["constant_2025_dollars"][name]={
                    "series_id":series[name]["series_id"],"factor":factor,
                    "total_salary_per_student_fte":g["total_salary_per_student_fte"]*factor,
                    "employer_compensation_per_student_fte":g["employer_compensation_per_student_fte"]*factor}
        out.append({"school_year":sy,"student_fte":students,
                    "strict_central_administration":strict,
                    "school_administration":school_g,
                    "central_plus_school_administration":combined})
    return {"schema_version":1,
      "definition":{"strict_central_administration":["district/central administration"],
        "school_administration":["principals/APs"],
        "excluded_ambiguous_management":"Director/Supervisor remains in other classified because public Duty Title cannot identify operating function."},
      "enrollment_denominator":"OSPI P-223 final annual-average K-12 student FTE including ALE",
      "years":out}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json")
    p.add_argument("--enrollment",default="artifacts/normalization/enrollment.json"); p.add_argument("--cpi",default="artifacts/normalization/cpi.json")
    p.add_argument("--output",default="artifacts/normalized/admin-overhead.json"); a=p.parse_args()
    r=build(json.loads(Path(a.metrics).read_text()),json.loads(Path(a.enrollment).read_text()),json.loads(Path(a.cpi).read_text()))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(r,indent=2)+"\n")
    for x in r["years"]:
        c=x["strict_central_administration"]; both=x["central_plus_school_administration"]
        print(f"{x['school_year']}: central=${c['employer_compensation_per_student_fte']:.2f}/student ({c['fte_per_1000_student_fte']:.2f} FTE/1000); central+school=${both['employer_compensation_per_student_fte']:.2f}/student")
if __name__=="__main__": main()
