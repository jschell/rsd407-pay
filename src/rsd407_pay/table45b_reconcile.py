from __future__ import annotations
import argparse,json
from decimal import Decimal
from pathlib import Path
DISTRICT_CODE="17407"; COMPONENT_ROUNDING_TOLERANCE=Decimal("0.015")
def reconcile(controls,metrics):
    by_year={r["school_year"]:r for r in metrics["district"]}; rows=[]
    for src in controls["years"]:
        year=src["school_year"]; control=src["table45b"]; project=Decimal(str(by_year[year]["total_fte"])); published=Decimal(str(control["total_fte"]))
        difference=published-project; status="pass" if abs(difference)<=COMPONENT_ROUNDING_TOLERANCE else "fail"
        rows.append({"school_year":year,"source_sha256":src["source_sha256"],"ospi_table45b":control,"project_total_fte":float(project),"difference_fte":float(difference),"comparison":"within_sum_of_three_hundredth-rounded_components","tolerance_fte":float(COMPONENT_ROUNDING_TOLERANCE),"status":status})
    return {"schema_version":2,"control":"OSPI Personnel Summary Table 45B","district_code":DISTRICT_CODE,"source_mode":"committed_reviewed_control","status":"pass" if all(r["status"]=="pass" for r in rows) else "fail","years":rows}
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument("--controls",default="controls/personnel-summary-published.json");p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json");p.add_argument("--output",default="artifacts/reconciliation/table45b-reconciliation.json");a=p.parse_args(argv)
    report=reconcile(json.loads(Path(a.controls).read_text()),json.loads(Path(a.metrics).read_text()));Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(report,indent=2)+"\n");print(json.dumps(report,indent=2));raise SystemExit(0 if report["status"]=="pass" else 1)
if __name__=="__main__":main()
