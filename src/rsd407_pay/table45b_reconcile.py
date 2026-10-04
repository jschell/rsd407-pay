from __future__ import annotations
import argparse,json,re
from decimal import Decimal
from pathlib import Path
from .personnel_pdf import DISTRICT_CODE,pdf_text,table_district_rows

TABLE_MARKER="Table 45B"
COMPONENT_ROUNDING_TOLERANCE=Decimal("0.015")

def parse_table45b_text(text: str) -> dict:
    row=table_district_rows(text,TABLE_MARKER)[0]
    vals=[Decimal(x.replace(",","")) for x in re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?",row)]
    if not vals or vals[0]!=Decimal(DISTRICT_CODE): raise RuntimeError("district code not first numeric field")
    fields=vals[1:]
    if len(fields)!=10: raise RuntimeError(f"unexpected Table 45B row layout: {len(fields)} numeric fields after district code")
    staff=[fields[1],fields[4],fields[7]]
    return {"certificated_instructional_fte":float(staff[0]),"certificated_administrative_fte":float(staff[1]),"classified_fte":float(staff[2]),"total_fte":float(sum(staff))}

def extract(pdf: Path) -> dict: return parse_table45b_text(pdf_text(pdf))

def reconcile(manifest: dict, metrics: dict) -> dict:
    by_year={r["school_year"]:r for r in metrics["district"]}; rows=[]
    for src in manifest["resources"]:
        year=src["school_year"]; control=extract(Path(src["local_file"])); project=Decimal(str(by_year[year]["total_fte"])); published=Decimal(str(control["total_fte"]))
        difference=published-project; status="pass" if abs(difference)<=COMPONENT_ROUNDING_TOLERANCE else "fail"
        rows.append({"school_year":year,"source_sha256":src["sha256"],"ospi_table45b":control,"project_total_fte":float(project),"difference_fte":float(difference),"comparison":"within_sum_of_three_hundredth-rounded_components","tolerance_fte":float(COMPONENT_ROUNDING_TOLERANCE),"status":status})
    return {"schema_version":2,"control":"OSPI Personnel Summary Table 45B","district_code":DISTRICT_CODE,"status":"pass" if all(r["status"]=="pass" for r in rows) else "fail","years":rows}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--manifest",default="artifacts/reconciliation/table47-source-manifest.json"); p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json"); p.add_argument("--output",default="artifacts/reconciliation/table45b-reconciliation.json"); a=p.parse_args(argv)
    report=reconcile(json.loads(Path(a.manifest).read_text()),json.loads(Path(a.metrics).read_text())); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2)); raise SystemExit(0 if report["status"]=="pass" else 1)
if __name__=="__main__": main()
