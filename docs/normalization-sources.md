# Normalization source collection

Plan 06 keeps normalization inputs independent from S-275 parsing.

## CPI

`python -m rsd407_pay.cpi` requests two BLS CPI-U All Items series from the BLS Public Data API and accepts only BLS-provided annual-average (`M13`) observations for 2014-2025:

- `CUUR0000SA0` — U.S. city average.
- `CUURS49DSA0` — Seattle-Tacoma-Bellevue, WA (current BLS area code S49D).

The collector requires all 12 annual-average observations for both series and fails rather than averaging monthly or bi-monthly observations locally. This is important because the national and Seattle series have different publication frequencies.

The output records the exact BLS series IDs, geography, retrieval time, source URL, and annual observations in `artifacts/normalization/cpi.json`.

Enrollment collection will be added separately after historical P-223 AAFTE download coverage is established.
