# Structured S-275 control derivation

## Evidence basis

The 2026-10-05 Access inventory run 37253674979 successfully inventoried all twelve final OSPI S-275 Access databases, 2013-14 through 2024-25. Each database exposes one public S-275 table. The core personnel and assignment fields are stable across the entire period; 2024-25 changes several numeric storage types but not their meaning.

## Source grain

The public Access table combines personnel-level fields and assignment-level fields. Personnel controls must therefore be deduplicated by the source personnel record identifier (`recno`) before aggregation. Assignment fields must not be used to allocate personnel salary or benefits unless a later control explicitly requires assignment analysis.

Personnel-level fields used for controls:
- district: `codist`
- source personnel record: `recno`
- certificated FTE: `certfte`
- classified FTE: `clasfte`
- certificated base salary: `certbase`
- classified base salary: `clasbase`
- other salary: `othersal`
- final total salary: `tfinsal`
- insurance benefits: `cins`
- mandatory benefits: `cman`

Assignment-level fields retained for diagnostics only:
- `parea`, `prog`, `act`, `darea`, `droot`, `dsufx`, `grade`, `bldgn`
- `asspct`, `assfte`, `asssal`, `asshpy`

## Derivation contract

For each school year:
1. Select exact district code 17407.
2. Group rows by `recno`.
3. Verify all personnel-level control fields are invariant within each `recno`; fail on disagreement rather than choosing a value.
4. Retain one personnel record per `recno`.
5. Derive:
   - certificated FTE = sum(`certfte`)
   - classified FTE = sum(`clasfte`)
   - total FTE = certificated + classified
   - certificated base salary = sum(`certbase`)
   - classified base salary = sum(`clasbase`)
   - base salary = certificated base + classified base
   - total salary = sum(`tfinsal`)
   - insurance = sum(`cins`)
   - mandatory benefits = sum(`cman`)
   - reported employer compensation = total salary + insurance + mandatory benefits
6. Preserve `othersal` as a separately reported diagnostic; do not assume its relationship to `tfinsal` without validating source semantics.
7. Record source URL, source/database SHA-256, table name, row count, unique personnel count, duplicate assignment-row count, derivation version, and field contract.

## Validation hierarchy

The structured Access database is an authoritative structured S-275 source but is not independent of S-275. Controls are checked in three layers:

1. Access-derived personnel controls versus the simplified public S-275 extract.
2. FTE versus independently published Personnel Summary Table 45B for 2019-20 through 2024-25. Existing accepted Table 45B totals are 342.19, 330.99, 340.62, 322.61, 322.50, and 337.36 FTE; the simplified extract differs by only 0.001-0.008 FTE.
3. Compensation versus published all-program Personnel Summary tables after structured totals are established. Published controls remain a separately identified external presentation/control source.

No PDF layout parsing is required by normal retained analysis. PDF extraction remains regeneration/evidence tooling only.
