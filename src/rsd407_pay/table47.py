from __future__ import annotations
import argparse,json
from pathlib import Path

DISTRICT_CODE="17407"
CONTROL_FIELDS={
 "student_fte":{"status":"comparable","project_field":"student_fte","note":"Independent cross-check against P-223 annual-average student FTE when Table 47 uses the same enrollment basis."},
 "certificated_fte":{"status":"candidate","project_field":"certificated_fte","note":"Compare only after Table 47 certificated-personnel scope is confirmed against simplified S-275 extract."},
 "classified_fte":{"status":"candidate","project_field":"classified_fte","note":"Compare only after Table 47 classified-personnel scope is confirmed against simplified S-275 extract."},
 "average_salary":{"status":"candidate","project_field":None,"note":"Do not compare to project salary/FTE until OSPI salary numerator and included personnel scope are confirmed."}
}

def build_control_inventory(personnel_inventory):
    resources=[]
    for r in personnel_inventory.get("resources",[]):
        label=r.get("label","").lower()
        if "table 47" in label:
            resources.append({"school_year":r["school_year"],"label":r["label"],"url":r["url"],"extension":r.get("extension")})
    return {"schema_version":1,"district_code":DISTRICT_CODE,"control_table":"OSPI Personnel Summary Table 47 — Selected Personnel Data by School District",
            "fields":CONTROL_FIELDS,"resources":resources,"covered_years":sorted({r["school_year"] for r in resources})}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--inventory",default="artifacts/reconciliation/personnel-summary-inventory.json"); p.add_argument("--output",default="artifacts/reconciliation/table47-control-inventory.json"); a=p.parse_args(argv)
    report=build_control_inventory(json.loads(Path(a.inventory).read_text()))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    print(f"Table 47 resources: {len(report['resources'])}; years={report['covered_years']}")
if __name__=="__main__": main()
