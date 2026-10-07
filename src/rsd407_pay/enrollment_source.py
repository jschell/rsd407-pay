from __future__ import annotations
import hashlib
import re
from .period import YEARS
import html as html_module
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser

LANDING_PAGE="https://ospi.k12.wa.us/safs-data-files"
LINK_TEXT="Final Enrollment Summary - For the School Years 2001-02 through 2024-2025"

@dataclass(frozen=True)
class Source:
    landing_page:str
    workbook_url:str

class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.href=None
        self.parts=[]
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a":
            self.href=dict(attrs).get("href")
            self.parts=[]
    def handle_data(self,data):
        if self.href is not None:
            self.parts.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self.href is not None:
            text=" ".join("".join(self.parts).split())
            self.links.append((text,self.href))
            self.href=None
            self.parts=[]

def discover(html:str)->Source:
    parser=_LinkParser()
    parser.feed(html_module.unescape(html))
    matches=[]
    for text, href in parser.links:
        label=re.fullmatch(r"Final Enrollment Summary - For the School Years (20\d{2})-(\d{2}) through (20\d{2})-(\d{4})", text)
        if not label:
            continue
        first, suffix, last, end = map(int, label.groups())
        if suffix != (first+1)%100 or end != last+1:
            continue
        if first <= int(YEARS[0][:4]) and last >= int(YEARS[-1][:4]):
            matches.append(href)
    if len(matches)!=1:
        raise RuntimeError(f"OSPI final enrollment summary link expected once, found {len(matches)}; title or required coverage may have changed")
    href=urllib.parse.urljoin(LANDING_PAGE,matches[0])
    parsed=urllib.parse.urlparse(href)
    if parsed.scheme!="https" or parsed.hostname!="ospi.k12.wa.us":
        raise RuntimeError(f"unexpected enrollment workbook host: {href}")
    if not parsed.path.lower().endswith(".xlsx"):
        raise RuntimeError(f"unexpected enrollment workbook format: {href}")
    return Source(LANDING_PAGE,href)

def sha256(data:bytes)->str: return hashlib.sha256(data).hexdigest()

def fetch_url(url:str)->bytes:
    req=urllib.request.Request(url,headers={"User-Agent":"rsd407-pay reproducible research"})
    with urllib.request.urlopen(req) as r: return r.read()

def fetch_source():
    html=fetch_url(LANDING_PAGE).decode("utf-8",errors="replace")
    source=discover(html)
    data=fetch_url(source.workbook_url)
    if len(data)<1000: raise RuntimeError("OSPI enrollment workbook download unexpectedly small")
    return source,data

