# Nearby district administration comparison

Read the [evaluation and sensitivity findings](evaluation.md) alongside the descriptive tables. It compares enrollment-size peers, evaluates the excluded-director scenario and school-count denominator, and separates accounting changes from causal or efficiency claims.

[Central-office comparison](comparison.md) uses retained final statewide S-275 and P-223 data for 2013-14, 2023-24, and 2024-25. [School administration per reporting school](school-administration.md) adds the official OSPI 2024-25 Report Card school enrollment dataset. [Annual district aggregates](comparison.csv) provide the three comparison years. JSON records preserve exact source hashes, URLs/paths, school lists, mapping additions, duty-title evidence and limitations.

Includes Riverview, Snoqualmie Valley, Northshore, Monroe, Sultan, Lakewood, Granite Falls, Tukwila, Orting, and Steilacoom Historical. Nearby and size peers are shown individually; no combined peer-average efficiency claim is made.

The generated central-office data come from successful workflow run [37719525723](https://github.com/jschell/rsd407-pay/actions/runs/37719525723). School-count enrichment was reproduced with `PYTHONPATH=src python -m rsd407_pay.peer_school_counts --root peer-results-final`; its JSON preserves retrieval time, exact API query and response hash. The workflow now runs both steps.

To reproduce: run **Central administration peer comparison** in GitHub Actions. The workflow selects immutable tags `s275-source-2026-10-02` and `normalization-source-2026-10-04`, then captures school-count data. To replay counts without a new request, run `rsd407_pay.peer_school_counts --root DIRECTORY --schools-json DIRECTORY/school-count-source.json`.

Strict central administration includes Superintendent, Deputy/Assist. Supt., and Other District Admin. Director/Supervisor is excluded because duties span operational functions; its FTE and compensation are shown separately. School administration includes principals, vice principals and Other School Admin. Previously unseen titles remain explicit review evidence. Peer totals have not undergone independent published-control reconciliation.

School counts include distinct codes with positive reported enrollment, including alternative/online/program schools. They are not physical campuses, and a program can share a principal. FTE per reporting school describes staffing distribution and does not establish necessity or efficiency.

Generate the evaluation with `PYTHONPATH=src python -m rsd407_pay.peer_evaluation`; the output records both input hashes and the evaluator hash. The peer workflow also regenerates it after school-count capture.
