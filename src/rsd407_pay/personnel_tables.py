from __future__ import annotations
import argparse, json, re, subprocess
from pathlib import Path

DISTRICT_CODE="17407"

def table_titles(pdf: Path) -> list[dict]:
    text=subprocess.run(["pdftotext","-layout",str(pdf),"-"],check=True,capture_output=True,text=True).stdout
    found=[]
    for m in re.finditer(r"(?m)^\s*(Table\s+\d+[^\n]*)$",text):
        title=" ".join(m.group(1).split())
        if title not in [x["title"] for x in found]: found.append({"title":title})
    return found

def inventory(manifest: dict) -> dict:
    rows=[]
    for src in manifest["resources"]:
        titles=table_titles(Path(src["local_file"]))
        rows.append({"school_year":src["school_year"],"source_sha256":src["sha256"],"tables":titles})
    return {"schema_version":1,"district_code":DISTRICT_CODE,"years":rows}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--manifest",default="artifacts/reconciliation/table47-source-manifest.json"); p.add_argument("--output",default="artifacts/reconciliation/personnel-table-inventory.json"); a=p.parse_args(argv)
    report=inventory(json.loads(Path(a.manifest).read_text())); Path(a.output).write_text(json.dumps(report,indent=2)+"\n")
    for y in report["years"]:
        print(y["school_year"]); [print("  "+t["title"]) for t in y["tables"]]
if __name__=="__main__": main()
