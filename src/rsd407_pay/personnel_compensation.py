from __future__ import annotations
import argparse,json,re,subprocess
from decimal import Decimal
from pathlib import Path

DISTRICT_CODE="17407"
TABLES=("Table 34B","Table 36B","Table 37C","Table 38B")
CERTIFICATED_COMPONENTS=("Table 34B","Table 36B")
CERTIFICATED_COMBINED="Table 37C"
CLASSIFIED="Table 38B"
ROW_RE=re.compile(r"^17407\\s+Riverview\\b")
NUM_RE=re.compile(r"\\d+(?:,\\d{3})*(?:\\.\\d+)?")

def _numbers(row: str) -> list[Decimal]:
    return [Decimal(x.replace(",","")) for x in NUM_RE.findall(row)]

def parse_row(row: str, marker: str) -> dict:
    vals=_numbers(row)
    if not vals or vals[0] != Decimal(DISTRICT_CODE): raise RuntimeError(f"unexpected {marker} district row")
    if len(vals)==10 and marker in CERTIFICATED_COMPONENTS: vals=vals[:4]+vals[5:]
    if len(vals)!=9: raise RuntimeError(f"unexpected {marker} row layout: {len(vals)} numeric fields")
    return {"individuals":int(vals[1]),"average_additional_salary_per_individual":float(vals[2]),"total_fte":float(vals[3]),
            "average_base_salary_per_fte":float(vals[4]),"average_total_salary_per_fte":float(vals[5]),
            "average_insurance_benefits_per_fte":float(vals[6]),"average_mandatory_benefits_per_fte":float(vals[7]),"days_in_1_fte":float(vals[8])}

def extract_table(text: str, marker: str) -> dict | None:
    candidates=[]
    for page_number,page in enumerate(text.split("\\f"),1):
        if marker not in page: continue
        candidates.extend((page_number,line.strip()) for line in page.splitlines() if ROW_RE.match(line.strip()))
    unique=list(dict.fromkeys(candidates))
    if not unique: return None
    if len(unique)!=1: raise RuntimeError(f"expected one Riverview row in {marker}, found {len(unique)}: {unique}")
    page,row=unique[0]; parsed=parse_row(row,marker); parsed.update({"table":marker,"pdf_page":page,"source_row":row}); return parsed

def _implied(row: dict, field: str) -> float: return row["total_fte"]*row[field]

def combine_certificated(parts: list[dict]) -> dict:
    fte=sum(x["total_fte"] for x in parts)
    out={"individuals":None,"average_additional_salary_per_individual":None,"total_fte":fte,"days_in_1_fte":None}
    for key in ("average_base_salary_per_fte","average_total_salary_per_fte","average_insurance_benefits_per_fte","average_mandatory_benefits_per_fte"):
        out[key]=sum(_implied(x,key) for x in parts)/fte if fte else None
    out["component_tables"]=[x["table"] for x in parts]; out["component_pages"]=[x["pdf_page"] for x in parts]; return out

def consolidated_crosscheck(combined: dict, parts: list[dict]) -> dict:
    component=combine_certificated(parts)
    fields=("average_base_salary_per_fte","average_total_salary_per_fte","average_insurance_benefits_per_fte","average_mandatory_benefits_per_fte")
    return {"fte_difference":combined["total_fte"]-component["total_fte"],
            "implied_total_differences":{k:_implied(combined,k)-_implied(component,k) for k in fields}}

def extract(pdf: Path) -> dict:
    text=subprocess.run(["pdftotext","-layout",str(pdf),"-"],check=True,capture_output=True,text=True).stdout
    found={m:extract_table(text,m) for m in TABLES}
    if found[CLASSIFIED] is None: raise RuntimeError(f"{CLASSIFIED} Riverview row not found")
    parts=[found[m] for m in CERTIFICATED_COMPONENTS]
    if any(x is None for x in parts): raise RuntimeError("certificated component table Riverview row not found")
    if found[CERTIFICATED_COMBINED] is not None:
        cert=found[CERTIFICATED_COMBINED]; method="Table 37C consolidated all-program certificated control"; crosscheck=consolidated_crosscheck(cert,parts)
    else:
        cert=combine_certificated(parts); method="FTE-weighted Table 34B instructional + Table 36B administrative controls"; crosscheck=None
    return {"certificated":cert,"classified":found[CLASSIFIED],"certificated_method":method,
            "certificated_component_controls":parts,"certificated_consolidated_crosscheck":crosscheck}

def inventory(manifest: dict) -> dict:
    rows=[{"school_year":s["school_year"],"source_sha256":s["sha256"],"controls":extract(Path(s["local_file"]))} for s in manifest["resources"]]
    return {"schema_version":2,"district_code":DISTRICT_CODE,
            "tables":{"certificated_components":CERTIFICATED_COMPONENTS,"certificated_combined":CERTIFICATED_COMBINED,"classified":CLASSIFIED},
            "years":rows,"comparison":{"status":"inventory_only_pending_public_extract_attribution_check"}}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--manifest",default="artifacts/reconciliation/table47-source-manifest.json"); p.add_argument("--output",default="artifacts/reconciliation/personnel-compensation-controls.json"); a=p.parse_args()
    report=inventory(json.loads(Path(a.manifest).read_text())); Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
