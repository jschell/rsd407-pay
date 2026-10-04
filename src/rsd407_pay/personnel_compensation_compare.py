from __future__ import annotations
import argparse,json
from pathlib import Path

FIELDS=("base_salary","total_salary","insurance_benefits","mandatory_benefits")
CONTROL_KEYS={
 "base_salary":"average_base_salary_per_fte","total_salary":"average_total_salary_per_fte",
 "insurance_benefits":"average_insurance_benefits_per_fte","mandatory_benefits":"average_mandatory_benefits_per_fte"}

def compare(controls,metrics):
    by_year={x["school_year"]:x for x in metrics["district"]}; years=[]
    for item in controls["years"]:
        year=item["school_year"]; project=by_year[year]; combined={}
        for field in FIELDS:
            key=CONTROL_KEYS[field]
            published=sum(float(item["controls"][kind]["total_fte"])*float(item["controls"][kind][key]) for kind in ("certificated","classified"))
            actual=float(project[field]); diff=actual-published
            combined[field]={"project_total":actual,"ospi_implied_total":published,"difference":diff,
                             "percent_difference":diff/published if published else None}
        years.append({"school_year":year,"source_sha256":item["source_sha256"],"combined_all_programs":combined})
    return {"schema_version":1,"district_code":controls["district_code"],
            "method":"sum(explicit certificated all-program control × published average/FTE, Table 38B classified control × published average/FTE)",
            "status":"evidence_only_pending_tolerance_and_rounding_assessment","years":years}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--controls",default="artifacts/reconciliation/personnel-compensation-controls.json"); p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json"); p.add_argument("--output",default="artifacts/reconciliation/personnel-compensation-comparison.json"); a=p.parse_args(argv)
    report=compare(json.loads(Path(a.controls).read_text()),json.loads(Path(a.metrics).read_text())); Path(a.output).write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
