from __future__ import annotations
import argparse,json
from decimal import Decimal
from pathlib import Path

FIELDS=("base_salary","total_salary","insurance_benefits","mandatory_benefits")
CONTROL_KEYS={"base_salary":"average_base_salary_per_fte","total_salary":"average_total_salary_per_fte","insurance_benefits":"average_insurance_benefits_per_fte","mandatory_benefits":"average_mandatory_benefits_per_fte"}

def product_rounding_bound(fte,average):
    f=Decimal(str(fte)); a=Decimal(str(average)); published=f*a
    lo=max(Decimal("0"),f-Decimal("0.005"))*max(Decimal("0"),a-Decimal("0.5"))
    hi=(f+Decimal("0.005"))*(a+Decimal("0.5"))
    return max(abs(published-lo),abs(hi-published))

def compare(controls,metrics):
    by_year={x["school_year"]:x for x in metrics["district"]}; years=[]
    for item in controls["years"]:
        year=item["school_year"]; project=by_year[year]; combined={}
        components=[*item["controls"]["certificated_components"],item["controls"]["classified"]]
        for field in FIELDS:
            key=CONTROL_KEYS[field]
            published=sum(Decimal(str(c["total_fte"]))*Decimal(str(c[key])) for c in components)
            bound=sum(product_rounding_bound(c["total_fte"],c[key]) for c in components)
            actual=Decimal(str(project[field])); diff=actual-published; inside=abs(diff)<=bound
            combined[field]={"project_total":float(actual),"ospi_implied_total":float(published),"difference":float(diff),
                             "percent_difference":float(diff/published) if published else None,"display_rounding_bound":float(bound),
                             "within_display_rounding_bound":inside,
                             "status":"pass" if field=="base_salary" and inside else ("fail" if field=="base_salary" else "semantic_review")}
        years.append({"school_year":year,"source_sha256":item["source_sha256"],
                      "certificated_control_tables":item["controls"]["certificated_control_tables"],
                      "classified_control_table":item["controls"]["classified"]["source_table"],
                      "combined_all_programs":combined})
    base_pass=all(y["combined_all_programs"]["base_salary"]["status"]=="pass" for y in years)
    return {"schema_version":3,"district_code":controls["district_code"],
            "method":"sum each published all-program component FTE × published average/FTE; certificated uses Table 37C when available, otherwise separate Table 34B + Table 36B; classified uses Table 38B",
            "base_salary_control_status":"pass" if base_pass else "fail",
            "other_compensation_status":"semantic_review_not_validation_gate",
            "status":"pass" if base_pass else "fail","years":years}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--controls",default="artifacts/reconciliation/personnel-compensation-controls.json"); p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json"); p.add_argument("--output",default="artifacts/reconciliation/personnel-compensation-comparison.json"); a=p.parse_args(argv)
    report=compare(json.loads(Path(a.controls).read_text()),json.loads(Path(a.metrics).read_text())); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2)); raise SystemExit(0 if report["status"]=="pass" else 1)
if __name__=="__main__": main()
