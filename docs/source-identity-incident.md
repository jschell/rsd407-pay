# Source identity incident

During Plan 03 inspection of the first all-final artifact, several downloaded workbooks were identified as F-196 accounting dictionaries rather than S-275 personnel data.

## Root cause

Plan 01 discovery scanned the entire SAFS page and selected the preferred file extension for a year without constraining candidates to the Personnel Reporting Data (S-275) section.

## Correction

Discovery is now scoped to the S-275 section and requires personnel/S-275 semantics in the link label or path. Tests ensure an F-196 link for the same school year cannot be selected.

The initial all-final artifact from workflow run 36883646826 must not be used for analysis and should be treated as invalidated provenance.
