from __future__ import annotations
import argparse,json,re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request,urlopen

PAGE="https://ospi.k12.wa.us/policy-funding/school-apportionment/school-publications/personnel-summary-reports"
YEARS=[f"{y}-{str(y+1)[-2:]}" for y in range(2013,2025)]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.href=None; self.text=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            self.href=dict(attrs).get("href"); self.text=[]
    def handle_data(self,data):
        if self.href is not None: self.text.append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.href is not None:
            self.links.append((" ".join("".join(self.text).split()),self.href))
            self.href=None; self.text=[]

def fetch(url=PAGE):
    req=Request(url,headers={"User-Agent":"rsd407-pay/1.0"})
    with urlopen(req,timeout=60) as r: return r.read().decode("utf-8","replace")

def inventory(html,base=PAGE):
    p=Links(); p.feed(html); out=[]
    for text,href in p.links:
        label=text.strip()
        match=re.search(r"(20\d{2})[-–](\d{2})",label)
        if not match: continue
        year=f"{match.group(1)}-{match.group(2)}"
        if year not in YEARS: continue
        low=label.lower()
        if "personnel summary" not in low and "table 45" not in low and "table 47" not in low: continue
        url=urljoin(base,href)
        out.append({"school_year":year,"label":label,"url":url,"extension":Path(url.split("?")[0]).suffix.lower() or None})
    coverage=sorted({x["school_year"] for x in out})
    return {"schema_version":1,"source_page":base,"expected_years":YEARS,"covered_years":coverage,"resources":out}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--html"); p.add_argument("--output",default="artifacts/reconciliation/personnel-summary-inventory.json"); a=p.parse_args(argv)
    html=Path(a.html).read_text() if a.html else fetch()
    report=inventory(html)
    missing=sorted(set(YEARS)-set(report["covered_years"]))
    if missing: raise RuntimeError(f"personnel-summary discovery missing years: {missing}")
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    print(f"discovered {len(report['resources'])} personnel-summary resources across {len(report['covered_years'])} years")
if __name__=="__main__": main()
