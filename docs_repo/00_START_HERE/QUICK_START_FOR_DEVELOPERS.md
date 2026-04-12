# Quick Start For Developers

## The Fastest Useful Reading Path

If you want to become productive quickly, read these in order:

1. [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
2. [../FAQ.md](../FAQ.md)
3. [../02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](../02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
4. [../02_ARCHITECTURE/DATA_FLOW_END_TO_END.md](../02_ARCHITECTURE/DATA_FLOW_END_TO_END.md)
5. [../02_ARCHITECTURE/CANONICAL_MODEL.md](../02_ARCHITECTURE/CANONICAL_MODEL.md)
6. [../02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md](../02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md)
7. [../04_MAPPING_AND_FORMATS/PDF_FIELD_MAPPING.md](../04_MAPPING_AND_FORMATS/PDF_FIELD_MAPPING.md)
8. [../04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md](../04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md)
9. [../06_CONTRIBUTING/CODEBASE_TOUR.md](../06_CONTRIBUTING/CODEBASE_TOUR.md)

## If You Are Joining To Work On A Specific Area

| Area | Read first |
| --- | --- |
| UI and desktop behavior | [../02_ARCHITECTURE/UI_ARCHITECTURE.md](../02_ARCHITECTURE/UI_ARCHITECTURE.md) |
| PDF ingestion or OCR | [../02_ARCHITECTURE/PDF_INGESTION_FLOW.md](../02_ARCHITECTURE/PDF_INGESTION_FLOW.md), [../02_ARCHITECTURE/OCR_AND_SCAN_STRATEGY.md](../02_ARCHITECTURE/OCR_AND_SCAN_STRATEGY.md) |
| parser quality | [../02_ARCHITECTURE/PARSING_PIPELINE.md](../02_ARCHITECTURE/PARSING_PIPELINE.md), [../06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md](../06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md) |
| canonical model and merge behavior | [../02_ARCHITECTURE/CANONICAL_MODEL.md](../02_ARCHITECTURE/CANONICAL_MODEL.md), [../02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md](../02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md) |
| XML and `.esx` output | [../02_ARCHITECTURE/ESX_GENERATION_FLOW.md](../02_ARCHITECTURE/ESX_GENERATION_FLOW.md), [../06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md](../06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md) |
| debugging and tests | [../05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md](../05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md), [../05_TESTING_AND_DEBUG/TESTING_STRATEGY.md](../05_TESTING_AND_DEBUG/TESTING_STRATEGY.md) |

## First-Hour Checklist

1. Set up the local environment.
2. Run the app once.
3. Run the unit tests once.
4. Read the codebase tour.
5. Pick one subsystem before changing any code.

## Local Setup

From the repo root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Optional clean-environment smoke:

```powershell
.\scripts\Verify-Clean-Environment.ps1
```

## Run The App

```powershell
.\scripts\Run-App.ps1
```

Alternative:

```powershell
.\.venv\Scripts\python.exe .\run_app.py
```

## Run Validation

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall src run_app.py tests
```

## What Not To Break

- the parser/export separation
- deterministic output naming and XML structure
- clear user-facing errors for bad PDFs and bad output paths
- post-write ESX package validation
- the canonical estimate as the exporter input contract

## Strong First Contributions

- add or refine metadata patterns for real carrier layouts
- improve OCR-heavy line-item parsing
- add fixture-based regression tests
- improve export assumptions where backed by real ESX evidence

## Read Next

- [../06_CONTRIBUTING/CONTRIBUTING.md](../06_CONTRIBUTING/CONTRIBUTING.md)
- [../06_CONTRIBUTING/DEVELOPMENT_SETUP.md](../06_CONTRIBUTING/DEVELOPMENT_SETUP.md)
- [../06_CONTRIBUTING/PULL_REQUEST_GUIDELINES.md](../06_CONTRIBUTING/PULL_REQUEST_GUIDELINES.md)
