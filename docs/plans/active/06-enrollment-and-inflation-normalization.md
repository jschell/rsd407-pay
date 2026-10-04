# Plan 06 — Enrollment and inflation normalization

## Goal

Put staffing and compensation changes in student-load and purchasing-power context without mixing denominator or inflation semantics into S-275 parsing.

## Source decisions

### Enrollment

Use Washington OSPI P-223 fiscal enrollment as the authoritative enrollment family. P-223 is reported monthly by LEAs from September through June and contains both student headcount and FTE.

The analytical denominator will be documented explicitly rather than using a generic "enrollment" label. Preferred annual denominator is annual-average student FTE (AAFTE) when a reproducible district-level historical series can be obtained for every S-275 year. If full historical AAFTE cannot be reproduced from OSPI's downloadable data, stop and document the coverage gap rather than substituting October headcount silently.

RSD407 must be selected by an authoritative district identifier/name rule, not fuzzy text matching.

### Inflation

Use two U.S. Bureau of Labor Statistics CPI-U, All items series as parallel inflation lenses:

1. U.S. city average CPI-U — the standard national purchasing-power comparison.
2. Seattle-Tacoma-Bellevue CPI-U — the locally relevant metropolitan price-change comparison.

Neither series replaces the other. Normalized outputs must preserve both. Local CPI is more volatile and based on a smaller sample than the national series, so differences between the two are analytical context rather than evidence that one series is intrinsically more accurate.

Map each school year to its ending calendar year: 2013-14 -> 2014, ..., 2024-25 -> 2025. Express constant-dollar outputs in 2025 dollars, matching the ending calendar year of the latest completed S-275 school year.

Constant-dollar conversion:

    real_2025 = nominal * CPI_2025 / CPI_year

Preserve the CPI observation, series identity, calendar-year mapping, source URL, retrieval metadata, and transformation alongside derived values.

## Work

- Add reproducible OSPI enrollment-source discovery/collection and provenance.
- Establish annual RSD407 enrollment denominator coverage for all 12 S-275 years.
- Add both national and Seattle-Tacoma-Bellevue BLS CPI-U series and provenance.
- Establish a reproducible annual-average value for each series for every ending calendar year 2014-2025; do not assume identical publication frequency.
- Validate school-year -> calendar-year alignment and 2025-dollar conversion.
- Join enrollment/CPI only after both source series pass coverage checks.
- Compute employee rows per 1,000 students and staff FTE per 1,000 students.
- Compute nominal and 2025-dollar compensation trends.
- Compute payroll/compensation per student where denominator semantics support it.
- Keep source-series collection independent from S-275 workbook parsing.

## Guardrails

- Never label student headcount as FTE or vice versa.
- Never silently substitute October enrollment, Report Card enrollment, or another series for P-223 AAFTE.
- Do not interpolate missing enrollment or CPI years.
- Do not use either CPI series to fill gaps in the other.
- Report national-CPI-adjusted and Seattle-CPI-adjusted values as separate named measures.
- Every normalized output states denominator, CPI series, base year, and school-year/calendar-year mapping.
- Preserve nominal values alongside real values.

## Acceptance

- Enrollment and CPI inputs have authoritative source provenance and complete documented coverage, or the pipeline fails loudly.
- All 12 S-275 school years map to exactly one enrollment denominator, one national CPI observation, and one Seattle-Tacoma-Bellevue CPI observation.
- Per-1,000-student and per-student measures state whether the denominator is headcount or FTE.
- Constant-dollar outputs reproduce the documented BLS ratio method.
- A retained-snapshot analysis can regenerate normalized outputs without manual analytical edits.
