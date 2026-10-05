# Structured S-275 control derivation

## Evidence basis

The 2026-10-05 Access inventory run 37253674979 successfully inventoried all twelve final OSPI S-275 Access databases, 2013-14 through 2024-25. Each database exposes one public S-275 table. The core personnel and assignment fields are stable across the entire period; 2024-25 changes several numeric storage types but not their meaning.

## Source grain

The public Access table combines personnel-level fields and assignment-level fields. The source field `recno` is an assignment sequence, not a district-wide personnel identifier. The earlier grouping interpretation was rejected by the real 2013-14 database because unrelated employees share `recno=1`.

Empirical all-years validation established the usable personnel-bearing-row rule: for exact district `codist=17407`, select rows with `recno=1`. Discovery run 37257621152 observed all twelve years with zero errors; in every year the resulting row count exactly matched the accepted simplified-extract employee-row count and the summed certificated + classified FTE matched to floating-point precision.

Personnel-level fields used for controls:
- district: `codist`
- assignment sequence used to select the personnel-bearing row: `recno=1`
- certificated FTE: `certfte`
- classified FTE: `clasfte`
- certificated base salary: `certbase`
- classified base salary: `clasbase`
- other salary: `othersal`
- final total salary: `tfinsal`
- insurance benefits: `cins`
- mandatory benefits: `cman`

Assignment-level fields remain diagnostic only.

## Derivation contract

For each school year:
1. Select exact district code 17407.
2. Select the source personnel-bearing row where `recno=1`; do not group unrelated records by `recno`.
3. Require the all-years discovery invariant before accepted controls are generated.
4. Derive certificated/classified/total FTE, certificated/classified/base salary, total salary, insurance, mandatory benefits, and reported employer compensation.
5. Preserve `othersal` separately; do not assume its relationship to `tfinsal` without source-semantic evidence.
6. Record source/database SHA-256, table, source-row count, personnel-row count, additional-assignment-row count, and derivation version.
7. Compare regenerated results with `controls/s275-access-riverview.json`; any unexplained value or provenance drift fails verification.

Accepted derivation run 37259308473 produced all twelve years successfully. The committed controls are a same-S-275-system reproducibility control, not an independent external validation source.

## Validation hierarchy

The structured Access database is an authoritative structured S-275 source but is not independent of S-275. Controls are checked in three layers:

1. Access-derived personnel controls versus the simplified public S-275 extract.
2. FTE versus independently published Personnel Summary Table 45B for 2019-20 through 2024-25. Existing accepted Table 45B totals are 342.19, 330.99, 340.62, 322.61, 322.50, and 337.36 FTE; the simplified extract differs by only 0.001-0.008 FTE.
3. Compensation versus published all-program Personnel Summary tables after structured totals are established. Published controls remain a separately identified external presentation/control source.

No PDF layout parsing is required by normal retained analysis. PDF extraction remains regeneration/evidence tooling only.
