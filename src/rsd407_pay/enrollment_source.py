from __future__ import annotations
import hashlib,re
import urllib.request
from dataclasses import dataclass

LANDING_PAGE="https://ospi.k12.wa.us/safs-data-files"
LINK_TEXT="Final Enrollment Summary - For the School Years 2001-02 through 2024-2025"

@dataclass(frozen=True)
class Source:
    landing_page:str
    workbook_url:str

def discover(html:str)->Source:
    # Match the authoritative link by its published title, not by guessing a file path.
    pat=re.compile(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>\s*'+re.escape(LINK_TEXT)+r'\s*</a>',re.I)
    m=pat.search(html)
    if not m: raise RuntimeError("OSPI final enrollment summary link not found or title changed")
    href=m.group(1)
    if href.startswith("/"): href="https://ospi.k12.wa.us"+href
    if not href.startswith("https://ospi.k12.wa.us/"): raise RuntimeError(f"unexpected enrollment workbook host: {href}")
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
