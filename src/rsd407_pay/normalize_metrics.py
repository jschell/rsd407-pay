from __future__ import annotations
import argparse,json
from pathlib import Path

YEARS=[f"{y}-{str(y+1)[-2:]}" for y in range(2013,2025)]
MONEY=("base_salary","total_salary","reported_employer_compensation")
CPI=("national_cpi_u","seattle_cpi_u")

def build(metrics,enrollment,cpi):
    district={x["school_year"]:x for x in metrics["district"]}
    enroll={x["school_year"]:x for x in enrollment["years"]}
    if set(district)!=set(YEARS) or set(enroll)!=set(YEARS):
        raise RuntimeError("normalization requires exact 2013-14 through 2024-25 district and enrollment coverage")
    series=cpi.get("series",{})
    for name in CPI:
        if name not in series: raise RuntimeError(f"missing CPI series {name}")
        missing=[str(y) for y in range(2014,2026) if str(y) not in series[name]["values"]]
        if missing: raise RuntimeError(f"{name} missing years: {missing}")
    out=[]
    for sy in YEARS:
        d=district[sy]; e=enroll[sy]; students=float(e["student_fte"])
        if students<=0: raise RuntimeError(f"{sy} invalid student FTE {students}")
        end_year=int("20"+sy[-2:])
        row={"school_year":sy,"ending_calendar_year":end_year,
             "student_fte":students,
             "enrollment_measure":e["measure"],
             "employee_rows_per_1000_student_fte":d["employee_rows"]/students*1000,
             "staff_fte_per_1000_student_fte":d["total_fte"]/students*1000}
        for key in MONEY:
            nominal=float(d[key]); row[f"{key}_per_student_fte"]=nominal/students
        row["constant_2025_dollars"]={}
        for name in CPI:
            values=series[name]["values"]; current=float(values[str(end_year)]); base=float(values["2025"])
            factor=base/current
            adjusted={"series_id":series[name]["series_id"],"geography":series[name]["geography"],
                      "cpi_observation":current,"cpi_2025":base,"factor":factor}
            for key in MONEY:
                adjusted[key]=float(d[key])*factor
                adjusted[f"{key}_per_fte"]=(float(d[key])*factor/d["total_fte"]) if d["total_fte"] else None
                adjusted[f"{key}_per_student_fte"]=float(d[key])*factor/students
            row["constant_2025_dollars"][name]=adjusted
        out.append(row)
    return {"schema_version":1,"base_dollar_year":2025,
            "school_year_calendar_mapping":"school year maps to ending calendar year",
            "enrollment_denominator":"OSPI P-223 final annual-average K-12 student FTE including ALE",
            "inflation_formula":"nominal * CPI_2025 / CPI_ending_calendar_year",
            "years":out}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json")
    p.add_argument("--enrollment",default="artifacts/normalization/enrollment.json")
    p.add_argument("--cpi",default="artifacts/normalization/cpi.json")
    p.add_argument("--output",default="artifacts/normalized/normalized-metrics.json")
    a=p.parse_args()
    report=build(json.loads(Path(a.metrics).read_text()),json.loads(Path(a.enrollment).read_text()),json.loads(Path(a.cpi).read_text()))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    for r in report["years"]:
        print(f"{r['school_year']}: students={r['student_fte']:.2f} staff_fte_per_1000={r['staff_fte_per_1000_student_fte']:.2f} total_salary_per_student=${r['total_salary_per_student_fte']:.2f}")
if __name__=="__main__": main()
