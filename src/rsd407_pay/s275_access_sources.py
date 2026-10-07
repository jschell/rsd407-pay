from __future__ import annotations
import argparse,json,re,urllib.parse,urllib.request
from html.parser import HTMLParser
from pathlib import Path
PAGE="https://ospi.k12.wa.us/safs-data-files"
from .period import YEARS, require_coverage
UA="rsd407-pay/1.0"
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.href=None; self.text=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a": self.href=dict(attrs).get("href"); self.text=[]
    def handle_data(self,data):
        if self.href is not None: self.text.append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.href is not None:
            self.links.append((" ".join("".join(self.text).split()),self.href)); self.href=None; self.text=[]
def fetch(url=PAGE):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=60) as r: return r.read().decode("utf-8","replace")
def normalize_year(label):
    m=re.search(r"(20\d{2})\s*[-–]\s*(?:20)?(\d{2})",label)
    return f"{m.group(1)}-{m.group(2)}" if m else None
def inventory(html,base=PAGE):
    p=Links(); p.feed(html); resources=[]
    for label,href in p.links:
        low=label.lower()
        if "s-275" not in low or "personnel database" not in low or "final" not in low: continue
        year=normalize_year(label)
        if year not in YEARS: continue
        resources.append({"school_year":year,"label":label,"url":urllib.parse.urljoin(base,href),"source_class":"s275_access","status":"discovered"})
    by={r["school_year"]:r for r in resources}; missing=[y for y in YEARS if y not in by]
    return {"schema_version":1,"landing_page":PAGE,"publisher":"Washington Office of Superintendent of Public Instruction","dataset":"Final S-275 Personnel Database","source_class":"s275_access","resources":[by[y] for y in YEARS if y in by],"missing_years":missing,"status":"pass" if not missing else "fail"}
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--html"); p.add_argument("--output",default="artifacts/reconciliation/s275-access-source-inventory.json"); a=p.parse_args(argv)
    report=inventory(Path(a.html).read_text() if a.html else fetch()); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
    if report["status"]!="pass": raise SystemExit("missing required final S-275 Access source years")
if __name__=="__main__": main()

