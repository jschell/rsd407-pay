from __future__ import annotations
import argparse,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone

SERIES={
 "national_cpi_u":{"series_id":"CUUR0000SA0","geography":"U.S. city average","expected_periods":12},
 "seattle_cpi_u":{"series_id":"CUURS49DSA0","geography":"Seattle-Tacoma-Bellevue, WA","expected_periods":6},
}
YEARS=list(range(2014,2026))
API="https://api.bls.gov/publicAPI/v2/timeseries/data/"

def fetch():
    payload=json.dumps({"seriesid":[x["series_id"] for x in SERIES.values()],"startyear":"2014","endyear":"2025"}).encode()
    req=urllib.request.Request(API,data=payload,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req) as r: return json.load(r)

def parse(payload):
    if payload.get("status")!="REQUEST_SUCCEEDED": raise RuntimeError(f"BLS request failed: {payload.get('message')}")
    by_id={s["seriesID"]:s for s in payload["Results"]["series"]}
    out={}
    for name,meta in SERIES.items():
        s=by_id.get(meta["series_id"])
        if not s: raise RuntimeError(f"missing BLS series {meta['series_id']}")
        annual={}
        for year in YEARS:
            obs=[float(x["value"]) for x in s["data"] if int(x["year"])==year and x["period"].startswith("M") and x["period"]!="M13"]
            if len(obs)!=meta["expected_periods"]:
                raise RuntimeError(f"{name} {year} expected {meta['expected_periods']} periodic observations, found {len(obs)}")
            annual[str(year)]=sum(obs)/len(obs)
        out[name]={"series_id":meta["series_id"],"geography":meta["geography"],
          "measure":"arithmetic_mean_of_published_periodic_cpi_observations",
          "expected_periods_per_year":meta["expected_periods"],"values":annual}
    return out

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="artifacts/normalization/cpi.json"); a=ap.parse_args()
    report={"source":"U.S. Bureau of Labor Statistics Public Data API","source_url":API,
      "retrieved_at":datetime.now(timezone.utc).isoformat(),"series":parse(fetch())}
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
    for name,s in report["series"].items():
        print(f"{name}: {len(s['values'])} annual means, 2014-2025; series={s['series_id']} periods/year={s['expected_periods_per_year']}")
if __name__=="__main__": main()
