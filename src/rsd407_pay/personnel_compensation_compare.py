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
def published_components(controls):
    cert=controls["certificated"]
    cert_parts=[cert] if controls.get("certificated_consolidated_crosscheck") is not None else controls["certificated_component_controls"]
    return [*cert_parts,controls["classified"]]
def compare(controls,metrics):
    by_year={x["school_year"]:x for x in metrics["district"]}; years=[]
    for item in controls["years"]:
        year=item["school_year"]; project=by_year[year]; combined={}; components=published_components(item["controls"])
        for field in FIELDS:
            key=CONTROL_KEYS[field]
            published=sum(Decimal(str(x["total_fte"]))*Decimal(str(x[key])) for x in components)
            bound=sum(product_rounding_bound(x["total_fte"],x[key]) for x in components)
            actual=Decimal(str(project[field])); diff=actual-published; inside=abs(diff)<=bound
            combined[field]={"project_total":float(actual),"ospi_implied_total":float(published),"difference":float(diff),"percent_difference":float(diff/published) if published else None,
                             "display_rounding_bound":float(bound),"within_display_rounding_bound":inside,
                             "status":"pass" if field=="base_salary" and inside else ("fail" if field=="base_salary" else "semantic_review")}
        years.append({"school_year":year,"source_sha256":item["source_sha256"],"certificated_method":item["controls"]["certificated_method"],"combined_all_programs":combined})
    base_pass=all(y["combined_all_programs"]["base_salary"]["status"]=="pass" for y in years)
    return {"schema_version":3,"district_code":controls["district_code"],"base_salary_control_status":"pass" if base_pass else "fail",
            "other_compensation_status":"semantic_review_not_validation_gate","status":"pass" if base_pass else "fail","years":years}
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--controls",default="artifacts/reconciliation/personnel-compensation-controls.json"); p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json"); p.add_argument("--output",default="artifacts/reconciliation/personnel-compensation-comparison.json"); a=p.parse_args(argv)
    report=compare(json.loads(Path(a.controls).read_text()),json.loads(Path(a.metrics).read_text())); Path(a.output).write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2)); raise SystemExit(0 if report["status"]=="pass" else 1)
if __name__=="__main__": main()
