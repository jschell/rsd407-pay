from __future__ import annotations
import argparse, json, re, subprocess
from pathlib import Path

DISTRICT_CODE="17407"
TABLE_TITLE="Table 47: School Districts Ranked by FTE Enrollment (Report P-223)"

def extract_table47(pdf: Path) -> dict:
    info=subprocess.run(["pdfinfo",str(pdf)],check=True,capture_output=True,text=True).stdout
    pages=int(re.search(r"^Pages:\s+(\d+)",info,re.M).group(1)); start=max(1,pages-25)
    text=subprocess.run(["pdftotext","-f",str(start),"-l",str(pages),"-layout",str(pdf),"-"],check=True,capture_output=True,text=True).stdout
    pos=text.find(TABLE_TITLE)
    if pos < 0: raise RuntimeError(f"{pdf}: Table 47 title not found")
    section=text[pos:]
    matches=re.findall(r"^\s*(\d+)\s+17407\s+Riverview\s+([\d,]+)\s*$",section,re.M)
    if len(matches)!=1: raise RuntimeError(f"{pdf}: expected one Riverview Table 47 row, found {len(matches)}")
    rank,value=matches[0]; return {"rank":int(rank),"student_fte_rounded":int(value.replace(",",""))}

def reconcile(manifest: dict, enrollment: dict) -> dict:
    by_year={r["school_year"]:r for r in enrollment["years"]}; rows=[]
    for src in manifest["resources"]:
        x=extract_table47(Path(src["local_file"])); project=float(by_year[src["school_year"]]["student_fte"])
        expected=round(project); diff=x["student_fte_rounded"]-expected
        rows.append({"school_year":src["school_year"],"source_sha256":src["sha256"],"table":"47","district_code":DISTRICT_CODE,"ospi_student_fte_rounded":x["student_fte_rounded"],"project_student_fte":project,"project_student_fte_rounded":expected,"difference_after_rounding":diff,"status":"pass" if diff==0 else "fail"})
    status="pass" if all(r["status"]=="pass" for r in rows) else "fail"
    return {"schema_version":1,"control":TABLE_TITLE,"status":status,"rows":sorted(rows,key=lambda r:r["school_year"])}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--manifest",default="artifacts/reconciliation/table47-source-manifest.json"); p.add_argument("--enrollment",default="artifacts/normalization/enrollment.json"); p.add_argument("--output",default="artifacts/reconciliation/table47-reconciliation.json"); a=p.parse_args(argv)
    report=reconcile(json.loads(Path(a.manifest).read_text()),json.loads(Path(a.enrollment).read_text())); Path(a.output).write_text(json.dumps(report,indent=2)+"\n"); print(f"Table 47 reconciliation: {report['status']}")
    if report["status"]!="pass": raise SystemExit(1)
if __name__=="__main__": main()
