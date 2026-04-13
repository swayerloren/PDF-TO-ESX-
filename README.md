# PDF TO ESX AGENT

Open-source Windows desktop app and Python pipeline for converting insurance estimate PDFs into structured ESX/XML export artifacts.

`PDF TO ESX AGENT` is built for messy real-world insurance estimate packets. It combines PDF text extraction, OCR fallback, estimate parsing, canonical normalization, and deterministic ESX-style export in one local, inspectable workflow.

| At A Glance | Details |
| --- | --- |
| Helps | developers, estimators, restoration/roofing teams, and insurance-claims workflow builders |
| Converts | one or more insurance estimate PDFs into `*.esx`, `*.esx.xml`, and `*.canonical.json` |
| Handles | native-text PDFs, scan-heavy PDFs, OCR fallback, and multi-PDF estimate merges |
| Runs As | source app or packaged Windows executable |
| Current Maturity | real and validated, but still early in parser coverage and not a proprietary `XACTDOC.ZIPXML` writer |

## Start Here

| If you want to... | Start here |
| --- | --- |
| understand the project quickly | [docs_repo/00_START_HERE/PROJECT_OVERVIEW.md](docs_repo/00_START_HERE/PROJECT_OVERVIEW.md) |
| run the app from source | [Quick Start](#quick-start) |
| build the Windows executable | [docs/WINDOWS_EXE_BUILD.md](docs/WINDOWS_EXE_BUILD.md) |
| review packaged validation evidence | [docs/PACKAGED_APP_VALIDATION.md](docs/PACKAGED_APP_VALIDATION.md) |
| understand the architecture | [docs_repo/02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](docs_repo/02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md) |
| explore the full docs knowledge base | [docs_repo/00_START_HERE/README_DOCS_REPO.md](docs_repo/00_START_HERE/README_DOCS_REPO.md) |
| contribute | [CONTRIBUTING.md](CONTRIBUTING.md) and [docs_repo/06_CONTRIBUTING/CONTRIBUTING.md](docs_repo/06_CONTRIBUTING/CONTRIBUTING.md) |

## Why This Repo Exists

Insurance estimate PDFs are messy in the ways that matter most for automation:

- layouts vary by carrier and estimate source
- guide pages and summary pages can pollute parsing
- scanned packets often need OCR
- totals, line items, and supplements can conflict

This repo exists to provide a real local-first converter and a codebase that other developers can inspect, debug, and improve without relying on a black-box service.

## What The App Does

The app accepts estimate PDFs, detects whether pages are text-based or scan-heavy, applies OCR when useful, extracts structured estimate data, normalizes that data into a canonical estimate model, and then generates:

- `*.esx`
- `*.esx.xml`
- `*.canonical.json`

The pipeline is intentionally split between PDF ingestion, parsing, canonical normalization, export generation, and UI orchestration.

## Current Status

- current public release baseline: `v0.2.0`
- real and runnable today
- Windows-focused
- packaged Windows executable build available through PyInstaller
- still early in parser coverage and ESX compatibility evidence

## Core Capabilities

- drag-and-drop and file-picker PDF upload
- visible selected-file list and output-folder selection
- native-text vs scanned-page detection
- local OCR fallback for text-poor pages
- metadata, totals, line-item, and roof-measurement extraction
- canonical estimate merge for multi-PDF runs
- deterministic XML and `.esx` package output
- package validation before success is reported
- clear success, warning, and failure states in the UI

## Quick Start

Requirements:

- Windows
- Python 3.12+ available through `py -3`
- Tkinter support in the Python install

Setup:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run from source:

```powershell
.\scripts\Run-App.ps1
```

Alternative:

```powershell
.\.venv\Scripts\python.exe .\run_app.py
```

Optional clean-environment verification:

```powershell
.\scripts\Verify-Clean-Environment.ps1
```

## Windows Executable Build

Build the packaged Windows executable:

```powershell
.\scripts\Build-Windows-Exe.ps1
```

The packaged application is produced at:

- `dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`

Release/install guidance for non-developers:

- distribute the entire `dist\PDF-TO-ESX-Agent\` folder, not just the `.exe`
- zip that folder for handoff or release download
- users should unzip it to a normal writable location and launch `PDF-TO-ESX-Agent.exe`
- there is no installer yet; the `onedir` layout is intentional for reliability

Build details and troubleshooting:

- [docs/WINDOWS_EXE_BUILD.md](docs/WINDOWS_EXE_BUILD.md)
- [docs/PACKAGED_APP_VALIDATION.md](docs/PACKAGED_APP_VALIDATION.md)

## Architecture Summary

The main pipeline is:

`PDF files -> document loading/OCR -> structured extraction -> canonical estimate -> ESX/XML export`

Key runtime files:

| Area | File |
| --- | --- |
| repo launcher | `run_app.py` |
| app bootstrap | `src/pdf_to_esx_agent/app/bootstrap.py` |
| conversion orchestration | `src/pdf_to_esx_agent/core/conversion_service.py` |
| PDF ingestion | `src/pdf_to_esx_agent/parsing/document_loader.py` |
| page classification | `src/pdf_to_esx_agent/parsing/page_classifier.py` |
| structured parsing | `src/pdf_to_esx_agent/extract/estimate_parser.py` |
| canonical merge | `src/pdf_to_esx_agent/core/merge.py` |
| ESX writer | `src/pdf_to_esx_agent/export/esx_writer.py` |
| package validation | `src/pdf_to_esx_agent/export/validator.py` |
| desktop UI | `src/pdf_to_esx_agent/ui/main_window.py` |

## Output Artifacts

Each successful conversion writes:

- `*.esx`
  zip-based ESX-style package containing `XACTDOC.XML`, `canonical_estimate.json`, and `manifest.json`
- `*.esx.xml`
  readable XML payload for inspection and troubleshooting
- `*.canonical.json`
  canonical estimate data used to build the export

Source-mode default output:

- `sample_output/generated/`

Packaged-executable default output:

- `%USERPROFILE%\Documents\PDF TO ESX AGENT\generated`

## Docs Index

The long-term project knowledge base is now in [`docs_repo/`](docs_repo/).

Start here:

- [docs_repo/00_START_HERE/README_DOCS_REPO.md](docs_repo/00_START_HERE/README_DOCS_REPO.md)
- [docs_repo/00_START_HERE/QUICK_START_FOR_DEVELOPERS.md](docs_repo/00_START_HERE/QUICK_START_FOR_DEVELOPERS.md)
- [docs_repo/FAQ.md](docs_repo/FAQ.md)
- [docs_repo/02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](docs_repo/02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
- [docs_repo/02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md](docs_repo/02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md)
- [docs_repo/04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md](docs_repo/04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md)
- [docs_repo/06_CONTRIBUTING/CONTRIBUTING.md](docs_repo/06_CONTRIBUTING/CONTRIBUTING.md)
- [docs_repo/07_PROJECT_HISTORY/CHANGELOG.md](docs_repo/07_PROJECT_HISTORY/CHANGELOG.md)
- [docs_repo/ARCHITECTURE_DIAGRAM_NOTES.md](docs_repo/ARCHITECTURE_DIAGRAM_NOTES.md)
- [docs_repo/OPEN_SOURCE_HANDOFF_SUMMARY.md](docs_repo/OPEN_SOURCE_HANDOFF_SUMMARY.md)
- [docs_repo/09_RELEASE_AND_OPEN_SOURCE/PUBLIC_POSITIONING.md](docs_repo/09_RELEASE_AND_OPEN_SOURCE/PUBLIC_POSITIONING.md)
- [docs_repo/09_RELEASE_AND_OPEN_SOURCE/GITHUB_DISCOVERABILITY.md](docs_repo/09_RELEASE_AND_OPEN_SOURCE/GITHUB_DISCOVERABILITY.md)

Where to go by task:

| If you want to... | Read this |
| --- | --- |
| understand the product and why it exists | [docs_repo/00_START_HERE/PROJECT_OVERVIEW.md](docs_repo/00_START_HERE/PROJECT_OVERVIEW.md) |
| onboard as a contributor | [docs_repo/00_START_HERE/QUICK_START_FOR_DEVELOPERS.md](docs_repo/00_START_HERE/QUICK_START_FOR_DEVELOPERS.md) |
| understand runtime architecture | [docs_repo/02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](docs_repo/02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md) |
| understand OCR and ingestion | [docs_repo/02_ARCHITECTURE/PDF_INGESTION_FLOW.md](docs_repo/02_ARCHITECTURE/PDF_INGESTION_FLOW.md) |
| understand multi-PDF merge behavior | [docs_repo/02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md](docs_repo/02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md) |
| improve parser quality | [docs_repo/06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md](docs_repo/06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md) |
| change ESX output | [docs_repo/06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md](docs_repo/06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md) |
| debug failures | [docs_repo/05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md](docs_repo/05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md) |
| review project evolution | [docs_repo/07_PROJECT_HISTORY/CHANGELOG.md](docs_repo/07_PROJECT_HISTORY/CHANGELOG.md) |
| understand release status and next steps | [docs_repo/09_RELEASE_AND_OPEN_SOURCE/ROADMAP.md](docs_repo/09_RELEASE_AND_OPEN_SOURCE/ROADMAP.md) |
| improve the GitHub landing page or public positioning | [docs_repo/09_RELEASE_AND_OPEN_SOURCE/GITHUB_DISCOVERABILITY.md](docs_repo/09_RELEASE_AND_OPEN_SOURCE/GITHUB_DISCOVERABILITY.md) |

Implementation/build-phase docs that still matter:

- [docs/AGENT_ANALYSIS_FOR_PDF_TO_ESX.md](docs/AGENT_ANALYSIS_FOR_PDF_TO_ESX.md)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/ESX_MAPPING.md](docs/ESX_MAPPING.md)
- [docs/TESTING_NOTES.md](docs/TESTING_NOTES.md)
- [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md)
- [docs/FINAL_BUILD_STATUS.md](docs/FINAL_BUILD_STATUS.md)
- [docs/WINDOWS_EXE_BUILD.md](docs/WINDOWS_EXE_BUILD.md)
- [docs/PACKAGED_APP_VALIDATION.md](docs/PACKAGED_APP_VALIDATION.md)

## Contributor Direction

If you want to:

- understand the app first, read `docs_repo/00_START_HERE/`
- improve parser quality, read `docs_repo/02_ARCHITECTURE/PARSING_PIPELINE.md` and `docs_repo/06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md`
- improve multi-PDF merge behavior, read `docs_repo/02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md`
- improve ESX output, read `docs_repo/02_ARCHITECTURE/ESX_GENERATION_FLOW.md` and `docs_repo/06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md`
- debug a failure, read `docs_repo/05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md`
- understand project evolution, read `docs_repo/07_PROJECT_HISTORY/`

Public contributor entry points:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SUPPORT.md](SUPPORT.md)
- [ROADMAP.md](ROADMAP.md)

## Validation Status

The current codebase has been validated with:

- automated tests in `tests/`
- `python -m compileall`
- clean-environment reinstall and UI startup smoke
- packaged executable startup smoke
- packaged executable real conversion smoke
- copied-release-folder packaged validation from a temp path outside the repo
- real estimate-PDF conversion runs against multiple source-agent fixtures

See:

- [docs/TESTING_NOTES.md](docs/TESTING_NOTES.md)

## Current Limitations

- the `.esx` package is standards-based, not a native proprietary `XACTDOC.ZIPXML` writer
- parser coverage is meaningful but still heuristic
- OCR-heavy layouts remain the weakest extraction area
- the packaged build is Windows-only and uses an `onedir` distribution for reliability

See:

- [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md)
- [docs_repo/03_ENGINEERING_DECISIONS/KNOWN_GAPS_AND_RISKS.md](docs_repo/03_ENGINEERING_DECISIONS/KNOWN_GAPS_AND_RISKS.md)

## Support And Security

- support and issue-routing guidance: [SUPPORT.md](SUPPORT.md)
- security reporting: [SECURITY.md](SECURITY.md)
- contributor expectations: [CONTRIBUTING.md](CONTRIBUTING.md)
- community behavior: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Roadmap

Current priorities and limits:

- [ROADMAP.md](ROADMAP.md)
- [docs_repo/09_RELEASE_AND_OPEN_SOURCE/OPEN_SOURCE_READINESS.md](docs_repo/09_RELEASE_AND_OPEN_SOURCE/OPEN_SOURCE_READINESS.md)

## License

Released under the Apache License 2.0.

See:

- [LICENSE](LICENSE)
- [OPEN_SOURCE_PHILOSOPHY.md](OPEN_SOURCE_PHILOSOPHY.md)
