# Changelog

All notable public-facing changes to `PDF TO ESX AGENT` should be documented here.

This root changelog is the public release summary. Deeper architectural and decision history lives in [docs_repo/07_PROJECT_HISTORY/](docs_repo/07_PROJECT_HISTORY/).

## [0.2.0] - 2026-04-12

Windows packaging and release-hardening milestone.

### Added

- PyInstaller-based Windows `onedir` packaging with a checked-in spec file
- repeatable build scripts for PowerShell and batch launch
- packaged-app validation documentation and packaged release guidance
- frozen-mode runtime tests covering user-writable logs and output paths

### Changed

- frozen-mode path handling now prefers Windows known folders before environment fallbacks
- packaged logging is file-only and writes to `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`
- packaged builds no longer create the default output folder at startup
- packaging cleanup removes transient metadata directories from the final bundle
- root and release docs now describe how to distribute the full `onedir` folder safely

### Validation

- packaged GUI startup smoke
- packaged conversion smoke with explicit output path
- packaged conversion smoke with default output path
- copied-release-folder validation from a temp path outside the repo
- no new `conhost.exe` process observed during packaged GUI launch
- unit tests and compile validation remained green

### Known Limitations At This Release

- distribution is still a Windows `onedir` folder, not an installer
- the executable is not yet signed
- some shells do not report useful exit codes for the windowed validation mode

## [0.1.0] - 2026-04-12

Initial public foundation release.

### Added

- runnable Windows desktop app for converting one or more insurance estimate PDFs
- drag-and-drop upload, file list, output folder selection, preview/status panels, and clear success or failure states
- local PDF ingestion with text extraction and selective OCR routing
- structured extraction for metadata, totals, line items, and roof-related measurements
- canonical estimate model and multi-PDF merge layer
- deterministic XML and `.esx` package generation
- package validation before success is reported
- automated tests for core output and conversion failure paths
- `docs_repo/` knowledge base for architecture, mapping, testing, contribution, and release guidance
- public-repo governance files, GitHub templates, and lightweight validation workflows
- PyInstaller-based Windows executable build with repeatable scripts and a checked-in spec file

### Improved Before Public Release

- parsing reliability across multiple real estimate layouts
- error messages for bad PDFs, empty parses, and invalid output paths
- warning visibility for scanned pages, totals fallback, and weak extraction cases
- logging consistency across validation, parsing, OCR, merge, and export stages
- contributor onboarding and release-readiness documentation
- frozen-mode runtime handling for logs, output paths, and packaged validation

### Known Limitations At This Release

- `.esx` output is a standards-based package, not a native proprietary `XACTDOC.ZIPXML` writer
- parser coverage is useful but not universal
- OCR-heavy layouts remain the weakest extraction area
- the packaged distribution is a Windows `onedir` artifact, not an installer
