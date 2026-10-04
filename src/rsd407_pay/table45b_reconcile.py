from __future__ import annotations
import argparse, json, re, subprocess
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

DISTRICT_CODE="17407"
TABLE_MARKER="Table 45B"

def parse_table45b_text(text: str) -> dict:
    pos=text.find(TABLE_MARKER)
    if pos < 0: raise RuntimeError("Table 45B not found")
    section=text[pos:]
    lines=[x for x in section.splitlines() if DISTRICT_CODE in x and "Riverview" in x]
    if len(lines)!=1: raise RuntimeError(f"expected one Riverview row in Table 45B, found {len(lines)}")
    nums=re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?",lines[0])
    vals=[Decimal(x.replace(",","")) for x in nums]
    if not vals or vals[0] != Decimal(DISTRICT_CODE): raise RuntimeError("district code not first numeric field")
    # Table 45B row ends with instructional certificated, administrative certificated, classified FTE, student FTE, ratios.
    # Select FTE fields structurally from the first three decimal-valued staff measures after the district code.
    staff=[v for v in vals[1:] if v.as_tuple().exponent < 0][:3]
    if len(staff)!=3: raise RuntimeError("could not identify three Table 45B staff FTE fields")
    return {"certificated_instructional_fte":float(staff[0]),"certificated_administrative_fte":float(staff[1]),"classified_fte":float(staff[2]),"total_fte":float(sum(staff))}

def extract(pdf: Path) -> dict:
    text=subprocess.run(["pdftotext","-layout",str(pdf),"-"],check=True,capture_output=True,text=True).stdout
    return parse_table45b_text(text)

def q2(v) -> Decimal: return Decimal(str(v)).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

def reconcile(manifest: dict, metrics: dict) -> dict:
    by_year={r["school_year"]:r for r in metrics["district"]}
    rows=[]
    for src in manifest["resources"]:
        year=src["school_year"]; control=extract(Path(src["local_file"])); project=Decimal(str(by_year[year]["total_fte"])); published=Decimal(str(control["total_fte"]))
        difference=published-project; status="pass" if q2(project)==q2(published) else "fail"
        rows.append({"school_year":year,"source_sha256":src["sha256"],"ospi_table45b":control,"project_total_fte":float(project),"difference_fte":float(difference),"comparison":"rounded_to_published_hundredth","status":status})
    return {"schema_version":1,"control":"OSPI Personnel Summary Table 45B","district_code":DISTRICT_CODE,"status":"pass" if all(r["status"]=="pass" for r in rows) else "fail","years":rows}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--manifest",default="artifacts/reconciliation/table47-source-manifest.json"); p.add_argument("--metrics",default="artifacts/normalized/annual-metrics.json"); p.add_argument("--output",default="artifacts/reconciliation/table45b-reconciliation.json"); a=p.parse_args(argv)
    report=reconcile(json.loads(Path(a.manifest).read_text()),json.loads(Path(a.metrics).read_text())); Path(a.output).write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2)); raise SystemExit(0 if report["status"]=="pass" else 1)
if __name__=="__main__": main()
