# Plan 10 — Evaluate opportunities to reduce recurring overhead outlay

## Goal and decision

Identify evidence-supported ways Riverview School District 407 could reduce recurring administration and IT expenditures while preserving required functions and service quality. Produce a bounded investigation and reviewable options, with net savings estimates only where evidence supports them.

Status: queued; created 2026-10-08. This plan extends the completed overhead survey. It does not implement district changes or promise savings.

## Starting evidence and limits

Use the reproducible [overhead review](../../comparisons/overhead-review.md), [findings](../../comparisons/overhead-findings.md), [financial source manifest](../../comparisons/overhead-sources.json), and [public-document evidence](../../comparisons/overhead-public-documents.json).

Existing retained evidence covers F-196 actual expenditures for 2023–24 and 2024–25 across ten selected districts and S-275 staffing history. It can identify expenditure trends and peer differences. It cannot isolate salaries versus contracts within each administration activity, establish workload, identify removable costs, or price replacement services.

The activity-based F-196 and duty-title-based S-275 measures have different coverage and accounting bases. Do not add them or interpret their difference as missing money. Peer spending gaps are investigation signals, not recoverable savings. District statements about reductions are not independently verified savings.

## Scope

First phase:
- F-196 activities 11–15: board, superintendent, business office, HR, and public relations.
- Activity 72: information systems, including relevant software and purchased services.
- Director/supervisor and clerical roles only where documented duties and location establish that they support these functions.
- Non-merger options: contract/license rationalization, cooperative purchasing, shared processing or services, process simplification, and role changes through attrition where supported.

Retain the existing nearby ten-district comparison; use its six size peers for the established size benchmark. Examine Snoqualmie Valley and Northshore as local service/practice examples while explicitly retaining their size differences.

Facilities, utilities, transportation, instructional staffing, and district mergers are outside this phase. Any expansion requires a separate scoped plan. Evaluate service and educational effects where overhead changes could affect them.

## Execution stages

### 1. Inventory available evidence before requesting records

- [ ] Search official OSPI, district, board, budget, audit, procurement, and regional service sources for detailed actuals, position budgets, contracts, and service agreements.
- [ ] Determine whether existing F-196 submissions or other downloadable reports provide activity-by-object detail; record availability rather than assume it is public.
- [ ] Build a source/gap register with document, district, period, coverage, URL, retrieval outcome, and intended question.
- [ ] Retain immutable source bytes where obtainable, with retrieval timestamp, SHA-256, source year, parser version, and page/row references. Record unavailable bytes and search-only evidence explicitly.
- [ ] List missing records precisely and draft targeted district records-request text. Sending requests requires a separate explicit user instruction.

Prioritize Riverview 2023–24 and 2024–25 actuals for activities 11–15 and 72. Extend to three to five comparable years only where available and useful. An unavailable year must remain a documented gap.

### 2. Explain changes in actual expenditures

- [ ] Obtain activity-by-object expenditure detail and relevant account/vendor detail; keep actuals distinct from budgets and forecasts.
- [ ] Reconcile detailed expenditure totals to retained F-196 activity totals. Explain differences, corrections, transfers, and fund boundaries; unresolved differences block dependent estimates.
- [ ] Separate compensation, purchased services, supplies, and other objects using documented codes.
- [ ] Identify recurring versus one-time items from source evidence, including legal, election, transition, or implementation expenses only if documented. Unknown causes remain unknown.
- [ ] Produce a change bridge attributing year-over-year changes to supported components, retaining an unexplained residual where necessary.
- [ ] Show nominal actuals for budget decisions; use the established CPI approach only for explicitly labeled historical comparisons.

### 3. Evaluate functions, contracts, and service alternatives

- [ ] Build a position/duty/location crosswalk with FTE, documented responsibilities, vacancies, and dates. Do not infer functions from employee names or titles alone.
- [ ] Obtain workload and service measures where available: payroll and AP transaction volumes, hiring/HR workload, users/endpoints, response times, backlogs, and service coverage.
- [ ] Inventory recurring contracts and software: vendor, scope, term, renewal/termination date, price, quantities, utilization evidence, and cancellation/transition obligations.
- [ ] Check duplication and license use only where functionality and actual usage are evidenced. A missing record is not evidence of non-use.
- [ ] Evaluate relevant PSESD, cooperative purchasing, and neighboring-district arrangements using signed scopes, published fees, or attributable quotes. Availability does not establish Riverview eligibility or benefit.
- [ ] Verify local reduction examples against implemented staffing and actual expenditures where possible; distinguish announcements, implementation, and measured outcomes.

Use only the detail necessary for analysis; publish aggregate roles and costs rather than unnecessary individual or confidential records.

### 4. Build and rank supported options

For each option, record:
- function and proposed change;
- evidence and current recurring cost;
- costs demonstrably removable, including timing and fixed costs that remain;
- recurring replacement/shared-service costs;
- one-time implementation, migration, training, severance, or capital costs where applicable;
- contract, labor, statutory, procurement, capacity, and service constraints supported by current authoritative sources;
- workload/service safeguards and measures to monitor;
- low/base/high assumptions, evidence confidence, dependencies, and unresolved questions.

Calculate recurring net savings as removable recurring costs minus new recurring costs. Calculate first-year net savings using realizable timing and one-time costs; report payback only where positive net recurring savings and sufficient inputs support it. Avoid overlapping savings across options.

Do not assume the peer median is an achievable target, every FTE reduction is a cash saving, automation removes a position, or spending shifts between funds/functions reduce districtwide outlay. Missing cost inputs yield an unquantified option or an explicitly conditional sensitivity analysis, not a claimed estimate.

Rank options by evidence strength, net benefit, feasibility, service effects, and implementation time. Unsupported options remain requests for evidence, not recommendations.

## Deliverables

Create a focused `docs/outlay-review/` evidence and analysis set:
1. Source inventory and gap register, with targeted records-request drafts if needed.
2. Reproducible baseline and expenditure-change tables, reconciliation results, and a data dictionary.
3. Functional staffing and contract/service inventories to the extent supported.
4. Options register with traceable calculations, assumptions, confidence, transition costs, and service effects.
5. Concise findings explaining what can be concluded, what remains unquantified, and the next decision.

Link substantive results from the README when available. Preserve source manifests and machine-readable outputs; keep interpretation separate from generated calculations.

## Validation and completion

- [ ] New parsers check hashes, schema drift, duplicates, missing periods, classification coverage, and reconciliation. Arithmetic checks cover timing, net costs, and overlapping options.
- [ ] Numerical outputs regenerate from retained inputs; CI verifies new calculations where implemented.
- [ ] Every material claim and proposed savings input points to evidence or a clearly marked assumption.
- [ ] Findings state years, cohort limits, coverage differences, and unresolved accounting/source issues.
- [ ] Complete the public-data screen and either produce supported options or document that required records prevent quantification. Completion does not require discovering a saving.
- [ ] Record evidence and limitations, then move this file to `docs/plans/complete/`.

Stop expanding collection when additional public sources no longer resolve a material decision. Publish the bounded screen and exact evidence gaps rather than prolonging research or filling gaps with guesses. District implementation and verification of achieved savings require subsequent authorized work.
