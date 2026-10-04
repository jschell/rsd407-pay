from __future__ import annotations
import argparse,json,re
from decimal import Decimal
from pathlib import Path
from .personnel_pdf import DISTRICT_CODE,pdf_text,table_district_rows

CLASSIFIED="Table 38B"
CERTIFICATED_COMBINED="Table 37C"
CERTIFICATED_LEGACY=("Table 34B","Table 36B")
NORMAL_FIELDS=("individuals","average_additional_salary_per_individual","total_fte","average_base_salary_per_fte","average_total_salary_per_fte","average_insurance_benefits_per_fte","average_mandatory_benefits_per_fte","days_in_1_fte")

def parse_control(text: str, marker: str) -> dict:
    row=table_district_rows(text,marker)[0]
    vals=[Decimal(x.replace(",","")) for x in re.findall(r"\\d+(?:,\\d{3})*(?:\\.\\d+)?",row)]
    if not vals or vals[0]!=Decimal(DISTRICT_CODE):
        raise RuntimeError(f"unexpected {marker} district row")
    payload=vals[1:]
    staff_mix=None
    if len(payload)==9:
        # 2019-20 certificated tables include a defunct Staff Mix value after Total FTE.
        staff_mix=payload.pop(3)
    if len(payload)!=8:
        raise RuntimeError(f"unsupported {marker} row schema: {len(vals)} numeric fields including district code")
    out=dict(zip(NORMAL_FIELDS,payload))
    out["individuals"]=int(out["individuals"])
    out={k:(float(v) if isinstance(v,Decimal) else v) for k,v in out.items()}
    out["staff_mix_defunct"]=float(staff_mix) if staff_mix is not None else None
    out["source_table"]=marker
    return out

def combine_certificated(parts: list[dict]) -> dict:
    fte=sum(x["total_fte"] for x in parts)
    out={"individuals":None,"average_additional_salary_per_individual":None,"total_fte":fte,"days_in_1_fte":None,"staff_mix_defunct":None,
         "source_table":" + ".join(x["source_table"] for x in parts)}
    for key in ("average_base_salary_per_fte","average_total_salary_per_fte","average_insurance_benefits_per_fte","average_mandatory_benefits_per_fte"):
        out[key]=sum(x["total_fte"]*x[key] for x in parts)/fte if fte else None
    return out

def extract(pdf: Path) -> dict:
    text=pdf_text(pdf)
    classified=parse_control(text,CLASSIFIED)
    if re.search(r"(?m)^\\s*"+re.escape(CERTIFICATED_COMBINED)+r":",text):
        certificated=parse_control(text,CERTIFICATED_COMBINED); structure=[CERTIFICATED_COMBINED]
    else:
        parts=[parse_control(text,m) for m in CERTIFICATED_LEGACY]
        certificated=combine_certificated(parts); structure=list(CERTIFICATED_LEGACY)
    return {"certificated":certificated,"classified":classified,"certificated_control_tables":structure}

def inventory(manifest: dict) -> dict:
    rows=[{"school_year":s["school_year"],"source_sha256":s["sha256"],"controls":extract(Path(s["local_file"]))} for s in manifest["resources"]]
    return {"schema_version":2,"district_code":DISTRICT_CODE,"source":"OSPI final Personnel Summary Reports",
            "tables":{"classified":CLASSIFIED,"certificated_combined":CERTIFICATED_COMBINED,"certificated_legacy":list(CERTIFICATED_LEGACY)},
            "comparison_status":"evidence_only_pending_rounding_assessment","years":rows}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--manifest",default="artifacts/reconciliation/table47-source-manifest.json"); p.add_argument("--output",default="artifacts/reconciliation/personnel-compensation-controls.json"); a=p.parse_args(argv)
    report=inventory(json.loads(Path(a.manifest).read_text())); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
