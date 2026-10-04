from __future__ import annotations
import argparse
import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

SERIES = {
    "national_cpi_u": {"series_id": "CUUR0000SA0", "geography": "U.S. city average", "expected_periods": 12},
    "seattle_cpi_u": {"series_id": "CUURS49DSA0", "geography": "Seattle-Tacoma-Bellevue, WA", "expected_periods": 6},
}
YEARS = list(range(2014, 2026))
API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

def _fetch_window(start: int, end: int):
    payload = json.dumps({"seriesid": [x["series_id"] for x in SERIES.values()], "startyear": str(start), "endyear": str(end)}).encode()
    req = urllib.request.Request(API, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        return json.load(response)

def fetch():
    payloads = [_fetch_window(2014, 2023), _fetch_window(2024, 2025)]
    merged = {"status": "REQUEST_SUCCEEDED", "Results": {"series": []}}
    for series_id in [x["series_id"] for x in SERIES.values()]:
        rows = []
        for payload in payloads:
            if payload.get("status") != "REQUEST_SUCCEEDED":
                raise RuntimeError(f"BLS request failed: {payload.get('message')}")
            matches = [x for x in payload["Results"]["series"] if x["seriesID"] == series_id]
            if len(matches) != 1:
                raise RuntimeError(f"BLS window missing series {series_id}")
            rows.extend(matches[0]["data"])
        keys = [(x["year"], x["period"]) for x in rows]
        if len(keys) != len(set(keys)):
            raise RuntimeError(f"duplicate BLS observations after window merge: {series_id}")
        merged["Results"]["series"].append({"seriesID": series_id, "data": rows})
    return merged

def parse(payload):
    if payload.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(f"BLS request failed: {payload.get('message')}")
    by_id = {series["seriesID"]: series for series in payload["Results"]["series"]}
    out = {}
    errors = []
    for name, meta in SERIES.items():
        series = by_id.get(meta["series_id"])
        if not series:
            errors.append(f"missing BLS series {meta['series_id']}")
            continue
        annual = {}
        for year in YEARS:
            period_rows = [x for x in series["data"] if int(x["year"]) == year and x["period"].startswith("M") and x["period"] != "M13"]
            invalid = [x for x in period_rows if x.get("value") in (None, "", "-")]
            obs = [float(x["value"]) for x in period_rows if x.get("value") not in (None, "", "-")]
            allowed_2025_october_gap = (
                year == 2025
                and len(invalid) == 1
                and invalid[0].get("period") == "M10"
                and invalid[0].get("value") == "-"
                and len(obs) == meta["expected_periods"] - 1
            )
            if invalid and not allowed_2025_october_gap:
                errors.append(f"{name} {year} nonnumeric: " + ", ".join(f"{x['period']}={x.get('value')!r}" for x in invalid))
            if len(obs) != meta["expected_periods"] and not allowed_2025_october_gap:
                errors.append(f"{name} {year} expected {meta['expected_periods']} numeric periodic observations, found {len(obs)}")
                continue
            annual[str(year)] = sum(obs) / len(obs)
        out[name] = {"series_id": meta["series_id"], "geography": meta["geography"],
                     "measure": "arithmetic_mean_of_published_periodic_cpi_observations",
                     "expected_periods_per_year": meta["expected_periods"], "values": annual,
                     "known_source_exceptions": {"2025": {"missing_period": "M10",
                         "reason": "BLS did not collect October 2025 CPI survey data during the federal appropriations lapse; no retroactive collection"}}}
    if errors:
        raise RuntimeError("BLS CPI coverage errors:\n" + "\n".join(errors))
    return out
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/normalization/cpi.json")
    args = ap.parse_args(argv)
    report = {"source": "U.S. Bureau of Labor Statistics Public Data API", "source_url": API,
              "retrieved_at": datetime.now(timezone.utc).isoformat(), "series": parse(fetch())}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    for name, series in report["series"].items():
        print(f"{name}: {len(series['values'])} annual means, 2014-2025; series={series['series_id']} periods/year={series['expected_periods_per_year']}")

if __name__ == "__main__":
    main()
