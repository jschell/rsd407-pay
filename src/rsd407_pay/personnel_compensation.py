from __future__ import annotations
import argparse,json,re,subprocess
from decimal import Decimal
from pathlib import Path
DISTRICT_CODE="17407"
TABLES={"certificated":"Table 37C","classified":"Table 38B"}
def parse_control(text: str, marker: str) -> dict:
    starts=[m.start() for m in re.finditer(r"(?m)^\s*"+re.escape(marker)+r":",text)]
    if not starts: raise RuntimeError(f"{marker} not found")
    lo=min(starts)
    next_table=re.search(r"(?m)^\s*Table\s+(?!"+re.escape(marker.replace("Table ",""))+r"\b)\d+[A-Z]?:",text[lo+1:])
    hi=len(text) if next_table is None else lo+1+next_table.start()
    lines=[x for x in text[lo:hi].splitlines() if x.lstrip().startswith(DISTRICT_CODE+" Riverview")]
    if len(lines)!=1: raise RuntimeError(f"expected one Riverview row in {marker}, found {len(lines)}")
    vals=[Decimal(x.replace(",","")) for x in re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?",lines[0])]
    if len(vals)<9 or vals[0]!=Decimal(DISTRICT_CODE): raise RuntimeError(f"unexpected {marker} row layout")
    return {"individuals":int(vals[1]),"average_additional_salary_per_individual":float(vals[2]),"total_fte":float(vals[3]),
            "average_base_salary_per_fte":float(vals[4]),"average_total_salary_per_fte":float(vals[5]),
            "average_insurance_benefits_per_fte":float(vals[6]),"average_mandatory_benefits_per_fte":float(vals[7]),"days_in_1_fte":float(vals[8])}
def extract(pdf: Path) -> dict:
    text=subprocess.run(["pdftotext","-layout",str(pdf),"-"],check=True,capture_output=True,text=True).stdout
    return {kind:parse_control(text,marker) for kind,marker in TABLES.items()}
def inventory(manifest: dict) -> dict:
    rows=[{"school_year":s["school_year"],"source_sha256":s["sha256"],"controls":extract(Path(s["local_file"]))} for s in manifest["resources"]]
    return {"schema_version":1,"district_code":DISTRICT_CODE,"source":"OSPI final Personnel Summary Reports","tables":TABLES,
            "comparison_status":"inventory_only_pending_public_extract_attribution_check","years":rows}
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--manifest",default="artifacts/reconciliation/table47-source-manifest.json"); p.add_argument("--output",default="artifacts/reconciliation/personnel-compensation-controls.json"); a=p.parse_args(argv)
    report=inventory(json.loads(Path(a.manifest).read_text())); Path(a.output).write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
