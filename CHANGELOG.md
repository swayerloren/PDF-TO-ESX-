# Changelog

All notable public-facing changes to `PDF TO ESX AGENT` should be documented here.

This root changelog is the public release summary. Deeper architectural and decision history lives in [docs_repo/07_PROJECT_HISTORY/](docs_repo/07_PROJECT_HISTORY/).

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

### Improved Before Public Release

- parsing reliability across multiple real estimate layouts
- error messages for bad PDFs, empty parses, and invalid output paths
- warning visibility for scanned pages, totals fallback, and weak extraction cases
- logging consistency across validation, parsing, OCR, merge, and export stages
- contributor onboarding and release-readiness documentation

### Known Limitations At This Release

- `.esx` output is a standards-based package, not a native proprietary `XACTDOC.ZIPXML` writer
- parser coverage is useful but not universal
- OCR-heavy layouts remain the weakest extraction area
- the project does not yet ship as an installer or standalone executable
