# Testing Notes

## Test Date

- April 12, 2026

## Environment

- Windows
- Python 3.12
- local virtual environment in `.venv`
- dependencies from `requirements.txt`

## Automated Checks

Commands run:

```powershell
.\.venv\Scripts\python.exe -m compileall src run_app.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\scripts\Verify-Clean-Environment.ps1
```

Current automated coverage includes:

- writer/package validation smoke test
- output-stem naming and filename sanitization coverage
- invalid PDF rejection smoke test
- missing-file, non-PDF, and invalid-output-folder rejection coverage
- clean-environment reinstall plus UI startup smoke test

## Real PDF Batch Validation

Source fixture location used:

- `C:\Users\LJ\AGENTS\SALES FORCE AGENT\TEST FILES\SCOPES`

Distinct estimate PDFs batch-converted:

| File | Result | Scan mode | Line items | Notes |
| --- | --- | --- | ---: | --- |
| `Adobe Scan Mar 25, 2026.pdf` | success with warning | native | 12 | letter + estimate bundle, totals reconstructed from parsed line items |
| `Adobe Scan Sep 9, 2025.pdf` | success with warning | scanned | 19 | OCR used across 13 pages, property address partially normalized |
| `debby_stewart_covington_scope.pdf` | success with warning | native | 26 | duplicate line item dedupe occurred |
| `JAMES DOWNS SCOPE.PDF` | success with warning | native | 29 | duplicate line item dedupe occurred |
| `KEMP- CARRIER SCOPE.pdf` | success with warning | native | 13 | carrier letter + estimate layout |
| `KUMAR SCOPE.pdf` | success | native | 11 | clean parse |
| `Mary Bereta ins scope.pdf` | success | native | 10 | clean parse |
| `Samuel Burgess insurance scope.pdf` | success with warning | native | 34 | duplicate line item dedupe occurred |
| `Statefarm estimate.pdf` | success | native | 12 | guide pages excluded correctly |
| `Tripathi Allstate original scope.pdf` | success | native | 21 | sample/guide pages excluded correctly |
| `Tripathi updated scope.pdf` | success | native | 22 | sample/guide pages excluded correctly |
| `Vaji Bhimani insurance scope (1).pdf` | success with warning | native | 27 | main validation sample |
| `Valencia SF Approval Estimate.pdf` | success with warning | native | 27 | duplicate line item dedupe occurred |

Batch summary:

- 13 of 13 distinct scope PDFs converted successfully
- 1 heavily scanned/OCR-driven sample converted successfully
- every generated `.esx` package passed post-write structure validation
- warning counts dropped materially after excluding carrier guide/sample pages and improving financial column parsing

## Representative Improvements Verified During Hardening

- sample/guide pages from Allstate and State Farm no longer pollute metadata and line items
- claim numbers and insured/property metadata improved on State Farm and mixed letter/estimate PDFs
- line-item financial parsing improved for tables that include depreciation percentages in the same row
- export validation now checks both XML well-formedness and zip package contents
- invalid/broken PDFs now fail through a user-facing conversion error path instead of silently exporting empty output

## Output Locations Used During Testing

- `sample_output/generated/`
- temporary batch-validation output folders created during engineering verification

The workspace is cleaned after validation runs, so large generated artifacts are not retained in the final repo state.

## Residual Issues Observed

- OCR-heavy Farmers scan still has incomplete insured extraction and a large summary-vs-line-item mismatch warning
- some carrier letter bundles provide incomplete estimate metadata, so `estimate_number` may remain unknown
- a few native PDFs still trigger warning-only dedupe events because duplicate line items appear across repeated pages/sections
