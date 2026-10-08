# Overhead review findings and next investigations

Review date: 2026-10-08 UTC (2026-10-07 Pacific). Financial observations cover 2023–24 and 2024–25; Riverview family staffing history covers 2013–14 through 2024–25. The ten-district cohort is selected, not representative of Washington.

## What changed in the evaluation

Riverview reported **$3,026,801** in F-196 actual general-fund activities 11–15, **5.1%** of its **$59,197,179** general-fund expenditures. This activity-based measure is **36.7% above** the selected six size-peer median per P-223 student FTE. It is higher per student than all nine other districts in this cohort.

This differs from the strict S-275 personnel-title measure, on which Riverview is below the size-peer median. F-196 includes spending on board, superintendent, business office, HR, and public relations across spending objects. S-275 identifies employees by reported duty title. **Do not add the two totals or describe their difference as missing money.** Neither measure includes every possible centrally managed function, and the F-196 measure excludes instructional supervision and information systems, which are displayed separately.

The activities 11–15 total increased **$346,074 (12.9%)** in the latest year. The largest increases within that group are business office, public relations, and board activities. Board activity covers expenditure charged to that function; it does not mean payments to elected board members. The aggregate workbook cannot distinguish salaries from legal, contractual, or other spending inside these individual activities.

The twelve-year history also changes the staffing interpretation: four strict central FTE in 2024–25 equals 2013–14 and 2019–20 and is below several intervening years. The increase follows 3.000 and 2.919 FTE in the previous two years. It is an increase from a low recent baseline, not evidence of unprecedented central staffing. Latest Director/Supervisor and clerical FTE also increased; their duties and locations are needed to determine which are central functions.

## Investigation priorities supported by this survey

| Priority | Evidence | Work needed to evaluate savings |
| --- | --- | --- |
| Business office | Large administration activity and largest dollar increase within activities 11–15 | Activity-by-object expenditure detail, payroll/AP workload, purchased-service contracts, staffing changes; compare shared-service fees with removable costs |
| Public relations and board support | Both show material latest-year increases | Separate recurring staffing/contracts from one-time legal, election, transition, or other expenses; do not assume any particular cause |
| HR and clerical allocation | Staffing titles cover school and district services | Position/location/workload crosswalk and vacancy history before considering shared processing or role consolidation |
| Information systems and software | Activity 72 is separately measured | License/contract inventory, utilization, renewal dates, existing cooperative agreements, transition costs; districtwide purchased services are not an IT spending total |
| Utilities | Latest expenditure rose while enrollment fell | Building area, meter consumption, tariff changes, operating hours, and capital alternatives; enrollment alone cannot establish excess energy use |

These priorities reflect observed spending and information gaps. They do not rank attainable savings. A zero in Printing or Instructional Technology does not establish that those services have no cost: spending may appear in another activity or fund.

## Public evidence of non-merger approaches

- **Riverview:** its [historical 2023 FAQ](https://www.rsd407.org/post/eagle-rock-multi-age-frequently-asked-questions-answered) describes clerical positions spanning schools and central support and cautions about coding and transportation comparisons. This supports requiring a functional crosswalk; it does not explain 2024–25 spending changes.
- **Monroe:** its [budget update](https://www.monroe.wednet.edu/about/news/news-details/~board/monroe-school-district/post/budget-update-financial-outlook) reports eliminating seven district-office positions, including three leadership roles, in recent years. This is district-reported implementation evidence, not an independently measured dollar saving.
- **Northshore:** its [December 11, 2023 announcement](https://www.nsd.org/resources/news-events/connections/post/~board/connections-newsletter/post/connections-december-11-2023) proposed removing 7.5 Administrative Center positions and adding 1.5 FTE to support reorganization, effective July 2024. The announced arithmetic is a net reduction of 6 FTE, not 7.5. It does not independently verify actual implementation or net expenditure savings.
- **Snoqualmie Valley:** its [2024–25 approved budget page](https://www.svsd410.org/departments/business-services/approved-district-budget) describes district-level reductions in operations, teaching and learning, and student services. The page does not isolate achieved overhead savings.
- **Regional options:** [PSESD](https://www.psesd.org/programs-services/administrative-management-services) offers administrative cooperatives and insurance pools. [Lake Washington's agreement list](https://www.lwsd.org/services/financial-services/intergovernmental-interlocal-cooperative-agreements) documents cooperative purchasing and interdistrict printing/cloud service arrangements. These establish mechanisms and local precedents, not Riverview participation or achievable savings.

Original public HTML downloads failed in this session; the above passages were reviewed through search-service retrieval. [Public-document evidence](overhead-public-documents.json) records URLs, retrieval limitations, and passage locations. The underlying budget presentations, job descriptions, signed agreements, vendor invoices, and implementation records were not reviewed. No complete contract inventory or functional duty allocation has been established for the four districts.

## Scope and completion

Completed: two-year actual financial comparison across all ten districts; three-year Director/Supervisor and clerical title survey; twelve-year Riverview central/clerical history; targeted public statements from four districts and regional service examples; source hashing, cross-sheet reconciliation, and parser checks.

The immediate next evidence to obtain is Riverview's **2023–24 and 2024–25 activity-by-object detail for activities 11–15 and 72**, plus a position/duty/location crosswalk and a recurring contract register. That would distinguish staffing, contracts, accounting allocation, and one-time changes. The current survey supports that focused review; it does not support a dollar savings commitment or a finding of waste.

## Reproduction

From the repository root, with requirements installed:

```bash
PYTHONPATH=src python -m rsd407_pay.overhead_review --peer docs/comparisons/comparison.json --annual-category docs/reporting/annual-category-detail.csv --sources docs/evidence/f196 --manifest docs/comparisons/overhead-sources.json --output docs/comparisons
python scripts/write_overhead_findings.py
```

The offline generator verifies retained workbook hashes, checks expected activity labels and year coverage, rejects duplicate/missing district rows, and reconciles district totals across Program, Activity, and Object sheets. Output JSON includes worksheet row locations, both enrollment measures, input hashes, and parser hash. Narrative findings are reviewed interpretation; numerical outputs are generated. Financial sources are actuals, not F-195 budgets. No new financial collection is attached to an existing automation workflow in this review.
