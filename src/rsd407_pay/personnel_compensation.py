from __future__ import annotations
import argparse,json,re,subprocess
from decimal import Decimal
from pathlib import Path
DISTRICT_CODE="17407"
CLASSIFIED="Table 38B"
CERTIFICATED_COMBINED="Table 37C"
CERTIFICATED_LEGACY=("Table 34B","Table 36B")
def parse_control(text: str, marker: str) -> dict:
    starts=[m.start() for m in re.finditer(r"(?m)^\s*"+re.escape(marker)+r":",text)]
    if not starts: raise RuntimeError(f"{marker} not found")
    lines=[]
    for lo in starts:
        tail=text[lo+1:]
        next_table=re.search(r"(?m)^\\s*Table\\s+\\d+[A-Z]?:",tail)
        hi=len(text) if next_table is None else lo+1+next_table.start()
        lines.extend(x for x in text[lo:hi].splitlines() if x.lstrip().startswith(DISTRICT_CODE+" Riverview"))
    lines=list(dict.fromkeys(lines))
    if len(lines)!=1: raise RuntimeError(f"expected one unique Riverview row in {marker}, found {len(lines)}")
    vals=[Decimal(x.replace(",","")) for x in re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?",lines[0])]
    if len(vals)<9 or vals[0]!=Decimal(DISTRICT_CODE): raise RuntimeError(f"unexpected {marker} row layout")
    return {"individuals":int(vals[1]),"average_additional_salary_per_individual":float(vals[2]),"total_fte":float(vals[3]),
            "average_base_salary_per_fte":float(vals[4]),"average_total_salary_per_fte":float(vals[5]),
            "average_insurance_benefits_per_fte":float(vals[6]),"average_mandatory_benefits_per_fte":float(vals[7]),"days_in_1_fte":float(vals[8])}
def combine_certificated(parts: list[dict]) -> dict:
    fte=sum(x["total_fte"] for x in parts)
    out={"individuals":None,"average_additional_salary_per_individual":None,"total_fte":fte,"days_in_1_fte":None}
    for key in ("average_base_salary_per_fte","average_total_salary_per_fte","average_insurance_benefits_per_fte","average_mandatory_benefits_per_fte"):
        out[key]=sum(x["total_fte"]*x[key] for x in parts)/fte if fte else None
    return out

def extract(pdf: Path) -> dict:
    text=subprocess.run(["pdftotext","-layout",str(pdf),"-"],check=True,capture_output=True,text=True).stdout
    classified=parse_control(text,CLASSIFIED)
    if re.search(r"(?m)^\\s*"+re.escape(CERTIFICATED_COMBINED)+r":",text):
        certificated=parse_control(text,CERTIFICATED_COMBINED); structure=[CERTIFICATED_COMBINED]
    else:
        parts=[parse_control(text,m) for m in CERTIFICATED_LEGACY]
        certificated=combine_certificated(parts); structure=list(CERTIFICATED_LEGACY)
    return {"certificated":certificated,"classified":classified,"certificated_control_tables":structure}
def inventory(manifest: dict) -> dict:
    rows=[{"school_year":s["school_year"],"source_sha256":s["sha256"],"controls":extract(Path(s["local_file"]))} for s in manifest["resources"]]
    return {"schema_version":1,"district_code":DISTRICT_CODE,"source":"OSPI final Personnel Summary Reports","tables":{"classified":CLASSIFIED,"certificated_combined":CERTIFICATED_COMBINED,"certificated_legacy":CERTIFICATED_LEGACY},
            "comparison_status":"inventory_only_pending_public_extract_attribution_check","years":rows}
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--manifest",default="artifacts/reconciliation/table47-source-manifest.json"); p.add_argument("--output",default="artifacts/reconciliation/personnel-compensation-controls.json"); a=p.parse_args(argv)
    report=inventory(json.loads(Path(a.manifest).read_text())); Path(a.output).write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
