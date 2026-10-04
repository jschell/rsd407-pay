# P-223 enrollment source discovery

## Selected source

OSPI's SAFS Data Files page publishes **Final Enrollment Summary - For the School Years 2001-02 through 2024-2025** under "Enrollment Data Files (P223/P223H)." OSPI describes these Excel files as summaries of student enrollment data at the Local Education Agency (LEA) level on the P-223 and P-223H forms.

Source landing page:

- https://ospi.k12.wa.us/safs-data-files

The fiscal enrollment documentation states that LEAs report P-223 enrollment monthly September through June using both headcount and FTE and that most LEA funding is based on annual average FTE (AAFTE).

## Plan 06 use

The final 2001-02 through 2024-25 workbook is the preferred historical source because a single OSPI-published final workbook covers every S-275 school year in scope.

The collector must:

1. discover the current workbook URL from the OSPI SAFS landing page rather than hard-code an inferred file path;
2. download it once per collection run;
3. record landing-page URL, resolved workbook URL, retrieval timestamp, SHA-256, and workbook identity;
4. inspect and validate its schema before extracting RSD407;
5. select Riverview using an authoritative district identifier when the workbook exposes one, otherwise use an exact documented district-name value;
6. extract the workbook's explicitly identified annual-average FTE measure only;
7. require exactly one final value for every school year 2013-14 through 2024-25;
8. fail on missing years, duplicate district-year observations, unexpected schema changes, or nonnumeric values.

Do not substitute Report Card/October headcount for missing P-223 AAFTE.

## Independent cross-check

OSPI Personnel Summary Reports Table 45B/47 use P-223 FTE student enrollment in staffing comparisons. These reports may be used as an independent validation source, but not as the primary enrollment dataset.
