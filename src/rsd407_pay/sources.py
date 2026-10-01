from __future__ import annotations
import argparse, hashlib, json, re, time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "rsd407-pay/0.1 (+https://github.com/jschell/rsd407-pay)"
YEAR_RE = re.compile(r"20\d{2}\s*[-–/]\s*(?:20)?\d{2}")

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self._href=None; self._text=[]
    def handle_starttag(self, tag, attrs):
        if tag=="a": self._href=dict(attrs).get("href"); self._text=[]
    def handle_data(self, data):
        if self._href is not None: self._text.append(data)
    def handle_endtag(self, tag):
        if tag=="a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href=None; self._text=[]

@dataclass
class Provenance:
    school_year:str; source_page_url:str; direct_download_url:str; file_format:str
    retrieved_at:str|None=None; sha256:str|None=None; byte_size:int|None=None
    http_status:int|None=None; content_type:str|None=None; parser_schema_version:int=1

def normalize_year(text:str)->str|None:
    m=YEAR_RE.search(text)
    if not m: return None
    nums=re.findall(r"\d+",m.group())
    a=int(nums[0]); b=int(nums[1]); b=b if b>99 else (a//100)*100+b
    return f"{a:04d}-{b%100:02d}"

def fetch(url:str, retries:int=3)->tuple[bytes,dict]:
    last=None
    for attempt in range(retries):
        try:
            req=Request(url,headers={"User-Agent":USER_AGENT,"Accept":"*/*"})
            with urlopen(req,timeout=60) as r:
                return r.read(), {"status":r.status,"content_type":r.headers.get("Content-Type",""),"final_url":r.geturl()}
        except (HTTPError,URLError,TimeoutError) as e:
            last=e
            if attempt+1<retries: time.sleep(2**attempt)
    raise RuntimeError(f"failed to fetch {url}: {last}")

def discover(config:dict)->list[Provenance]:
    body,meta=fetch(config["landing_page"])
    if b"<html" not in body[:1000].lower(): raise RuntimeError("OSPI landing page did not return HTML")
    p=Links(); p.feed(body.decode("utf-8","replace"))
    allowed=set(config["allowed_hosts"]); preferred=set(config["preferred_formats"]); found={}
    for href,text in p.links:
        url=urljoin(meta["final_url"],href); host=urlparse(url).hostname
        ext=Path(urlparse(url).path).suffix.lower().lstrip(".")
        year=normalize_year(text+" "+url)
        if host not in allowed or ext not in preferred or not year: continue
        if year not in config["expected_final_years"]: continue
        candidate=Provenance(year,config["landing_page"],url,ext)
        rank=config["preferred_formats"].index(ext)
        if year not in found or rank < found[year][0]: found[year]=(rank,candidate)
    return [found[y][1] for y in config["expected_final_years"] if y in found]

def validate_download(p:Provenance)->Provenance:
    body,meta=fetch(p.direct_download_url)
    ctype=meta["content_type"].lower()
    if len(body)<1024: raise RuntimeError(f"{p.school_year}: suspiciously small download ({len(body)} bytes)")
    if b"<html" in body[:1000].lower() or "text/html" in ctype:
        raise RuntimeError(f"{p.school_year}: expected data file but received HTML")
    p.retrieved_at=datetime.now(timezone.utc).isoformat()
    p.sha256=hashlib.sha256(body).hexdigest(); p.byte_size=len(body)
    p.http_status=meta["status"]; p.content_type=meta["content_type"]
    return p

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--config",default="config/sources.json")
    ap.add_argument("--output",default="artifacts/source-status.json"); ap.add_argument("--validate-downloads",action="store_true")
    args=ap.parse_args(argv); config=json.loads(Path(args.config).read_text())
    rows=discover(config); got={r.school_year for r in rows}; expected=set(config["expected_final_years"])
    missing=sorted(expected-got)
    if missing: raise SystemExit("Missing expected S-275 source years: "+", ".join(missing))
    if args.validate_downloads: rows=[validate_download(r) for r in rows]
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"generated_at":datetime.now(timezone.utc).isoformat(),"sources":[asdict(r) for r in rows]},indent=2)+"\n")
    print(f"validated discovery for {len(rows)} S-275 school years; wrote {out}")

if __name__=="__main__": main()
