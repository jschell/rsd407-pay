from __future__ import annotations
import argparse,json,re,subprocess
from decimal import Decimal
from pathlib import Path
DISTRICT_CODE="17407"; COMPONENT_ROUNDING_TOLERANCE=Decimal("0.015")
TABLE_MARKER="Table 45B"
def parse_table45b_text(text: str) -> dict:
    pos=text.find(TABLE_MARKER)
    if pos<0: raise RuntimeError("Table 45B not found")
    tail=text[pos:];next_table=re.search(r"(?m)^\\s*Table\\s+(?!45B\\b)\\d+[A-Z]?\\b",tail[len(TABLE_MARKER):]);section=tail if next_table is None else tail[:len(TABLE_MARKER)+next_table.start()]
    lines=[x for x in section.splitlines() if DISTRICT_CODE in x and "Riverview" in x]
    if len(lines)!=1: raise RuntimeError(f"expected one Riverview row in Table 45B, found {len(lines)}")
    vals=[Decimal(x.replace(",","")) for x in re.findall(r"\\d+(?:,\\d{3})*(?:\\.\\d+)?",lines[0])]
    if not vals or vals[0]!=Decimal(DISTRICT_CODE): raise RuntimeError("district code not first numeric field")
    fields=vals[1:]
    if len(fields)<10: raise RuntimeError(f"unexpected Table 45B row layout: {len(fields)} numeric fields after district code")
    staff=[fields[1],fields[4],fields[7]]
    return {"certificated_instructional_fte":float(staff[0]),"certificated_administrative_fte":float(staff[1]),"classified_fte":float(staff[2]),"total_fte":float(sum(staff))}
def extract(pdf: Path) -> dict:
    text=subprocess.run(["pdftotext","-layout",str(pdf),"-"],check=True,capture_output=True,text=True).stdout
    return parse_table45b_text(text)

def reconcile(controls,metrics):
    by_year={r["school_year"]:r for r in metrics["district"]}; rows=[]
    for src in controls["years"]:
        year=src["school_year"]; control=src["table45b"]; project=Decimal(str(by_year[year]["total_fte"])); published=Decimal(str(control["total_fte"]))
        difference=published-project; status="pass" if abs(difference)<=COMPONENT_ROUNDING_TOLERANCE else "fail"
        rows.append({"school_year":year,"source_sha256":src["source_sha256"],"ospi_table45b":control,"project_total_fte":float(project),"difference_fte":float(difference),"comparison":"within_sum_of_three_hundredth-rounded_components","tolerance_fte":float(COMPONENT_ROUNDING_TOLERANCE),"status":status})
    return {"schema_version":2,"control":"OSPI Personnel Summary Table 45B","district_code":DISTRICT_CODE,"source_mode":"committed_reviewed_control","status":"pass" if all(r["status"]=="pass" for r in rows) else "fail","years":rows}
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument("--controls",default="controls/personnel-summary-published.json");p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json");p.add_argument("--output",default="artifacts/reconciliation/table45b-reconciliation.json");a=p.parse_args(argv)
    report=reconcile(json.loads(Path(a.controls).read_text()),json.loads(Path(a.metrics).read_text()));Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(report,indent=2)+"\\n");print(json.dumps(report,indent=2));raise SystemExit(0 if report["status"]=="pass" else 1)
if __name__=="__main__":main()
