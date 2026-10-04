from __future__ import annotations
import re, subprocess
from pathlib import Path

DISTRICT_CODE="17407"

def pdf_text(pdf: Path) -> str:
    return subprocess.run(["pdftotext","-layout",str(pdf),"-"],check=True,capture_output=True,text=True).stdout

def table_district_rows(text: str, marker: str, district_code: str=DISTRICT_CODE, district_name: str="Riverview") -> list[str]:
    headings=[m.start() for m in re.finditer(r"(?m)^\\s*"+re.escape(marker)+r":",text)]
    if not headings:
        raise RuntimeError(f"{marker} not found")
    rows=[]
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if not re.match(r"^\\s*"+re.escape(marker)+r":",line):
            continue
        for candidate in lines[i+1:i+80]:
            if re.match(r"^\\s*Table\\s+\\d+[A-Z]?:",candidate):
                break
            if re.search(r"(^|\\s)"+re.escape(district_code)+r"\\s+"+re.escape(district_name)+r"\\b",candidate):
                rows.append(" ".join(candidate.split()))
    unique=list(dict.fromkeys(rows))
    if len(unique)!=1:
        raise RuntimeError(f"expected one unique {district_name} row in {marker}, found {len(unique)}")
    return unique
