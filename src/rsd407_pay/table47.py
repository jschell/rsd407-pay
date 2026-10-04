from __future__ import annotations
import argparse,json
from pathlib import Path

DISTRICT_CODE="17407"
CONTROL_FIELDS={"student_fte":{"status":"comparable","project_field":"student_fte","note":"Independent rounded P-223 annual-average student FTE control."}}

def build_control_inventory(personnel_inventory):
    resources=[]
    for r in personnel_inventory.get("resources",[]):
        # personnel_summary.inventory() already vetted these as annual Personnel Summary resources.
        # Table 47 is embedded in each PDF; link labels are not stable enough to re-filter.
        if r.get("extension")==".pdf":
            resources.append({"school_year":r["school_year"],"label":r["label"],"url":r["url"],"extension":r.get("extension"),"table":"47","source_mode":"embedded"})
    return {"schema_version":1,"district_code":DISTRICT_CODE,"control_table":"OSPI Personnel Summary Table 47 — School Districts Ranked by FTE Enrollment (Report P-223)",
            "fields":CONTROL_FIELDS,"resources":resources,"covered_years":sorted({r["school_year"] for r in resources})}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--inventory",default="artifacts/reconciliation/personnel-summary-inventory.json"); p.add_argument("--output",default="artifacts/reconciliation/table47-control-inventory.json"); a=p.parse_args(argv)
    report=build_control_inventory(json.loads(Path(a.inventory).read_text()))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    print(f"Table 47 resources: {len(report['resources'])}; years={report['covered_years']}")
if __name__=="__main__": main()
