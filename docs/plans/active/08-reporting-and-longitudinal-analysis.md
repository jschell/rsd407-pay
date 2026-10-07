# Plan 08 — Reporting and longitudinal analysis

## Goal

Publish a clear 2013-14 through latest-final view of RSD407 staffing and compensation.

## Outputs

- annual summary table;
- category detail table;
- baseline-to-latest change table;
- staffing per 1,000 students;
- nominal and real compensation trends;
- instructional vs school administration vs central administration trends;
- classified staffing trends;
- source/provenance appendix;
- limitations and category-definition notes.

## Initial questions

- Did staffing grow faster or slower than enrollment?
- Which job families gained/lost FTE?
- How did administration and instructional staffing change relative to one another?
- How did compensation change in nominal and real terms?
- Did the mix of certificated/classified work change?
- Are there structural breaks caused by coding/reporting changes rather than actual staffing changes?

## Acceptance

The report can be regenerated from the repository/workflow outputs without manually changing analytical numbers.

## Status

Active. The first implementation generates all reporting tables and narrative from gated retained-analysis outputs. It includes strict central-administration compensation per 1,000 student FTE with nominal, national-CPI and Seattle-CPI views. Inputs and generator code are SHA-identified, and Plan 07's source/semantic limitations are carried into the report.

Local validation: 70 unittest tests passed and report generation succeeded on retained outputs from run 37406368550. Full PR analysis must also generate and retain the report before this plan is moved to complete. No causal explanation of reporting breaks or payroll conditions is asserted.
