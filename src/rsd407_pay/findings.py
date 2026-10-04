from __future__ import annotations
import argparse, json
from pathlib import Path

START, END = "2013-14", "2024-25"

def change(a, b):
    return (b / a - 1) * 100

def build(metrics, normalized, admin, s275_tag, normalization_tag):
    district = {x["school_year"]: x for x in metrics["district"]}
    categories = {(x["school_year"], x["job_family"]): x for x in metrics["categories"]}
    norm = {x["school_year"]: x for x in normalized["years"]}
    adm = {x["school_year"]: x for x in admin["years"]}
    first, last = norm[START], norm[END]
    families = []
    for family in sorted({x["job_family"] for x in metrics["categories"]}):
        a, b = categories.get((START, family)), categories.get((END, family))
        if not a or not b:
            continue
        av = float(a["total_fte"]) / first["student_fte"] * 1000
        bv = float(b["total_fte"]) / last["student_fte"] * 1000
        families.append({"job_family": family, "start": av, "end": bv, "change": bv-av})
    families.sort(key=lambda x: x["change"], reverse=True)
    real = {}
    for cpi in ("national_cpi_u", "seattle_cpi_u"):
        real[cpi] = {}
        for key in ("total_salary_per_student_fte", "reported_employer_compensation_per_student_fte"):
            a = first["constant_2025_dollars"][cpi][key]
            b = last["constant_2025_dollars"][cpi][key]
            real[cpi][key] = {"start": a, "end": b, "percent_change": change(a,b)}
        for label, group in (("central", "strict_central_administration"), ("central_plus_school", "central_plus_school_administration")):
            a = adm[START][group]["constant_2025_dollars"][cpi]["employer_compensation_per_student_fte"]
            b = adm[END][group]["constant_2025_dollars"][cpi]["employer_compensation_per_student_fte"]
            real[cpi][label] = {"start": a, "end": b, "percent_change": change(a,b)}
    return {
        "schema_version": 1,
        "source_snapshots": {"s275": s275_tag, "normalization": normalization_tag},
        "period": {"start": START, "end": END},
        "student_fte": {"start": first["student_fte"], "end": last["student_fte"], "percent_change": change(first["student_fte"], last["student_fte"])},
        "staff_fte": {"start": district[START]["total_fte"], "end": district[END]["total_fte"], "percent_change": change(district[START]["total_fte"], district[END]["total_fte"])},
        "staff_fte_per_1000": {"start": first["staff_fte_per_1000_student_fte"], "end": last["staff_fte_per_1000_student_fte"], "percent_change": change(first["staff_fte_per_1000_student_fte"], last["staff_fte_per_1000_student_fte"])},
        "constant_2025_dollars": real,
        "job_family_staffing_intensity": families,
    }

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--s275-tag", required=True)
    p.add_argument("--normalization-tag", required=True)
    p.add_argument("--output", default="artifacts/normalized/longitudinal-findings.json")
    a=p.parse_args(argv)
    load=lambda name: json.loads(Path("artifacts/normalized", name).read_text())
    report=build(load("annual-metrics.json"), load("normalized-metrics.json"), load("admin-overhead.json"), a.s275_tag, a.normalization_tag)
    Path(a.output).write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
