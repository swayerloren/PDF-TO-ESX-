# Changelog

All notable changes to `PDF TO ESX AGENT` should be documented here.

The current repo is still early-stage, so version notes should stay honest about what is implemented, what is heuristic, and what is still assumed.

## v0.2.0 - 2026-04-12 - Windows Packaging Milestone

Release status:

- packaged Windows `onedir` build added
- frozen-mode runtime hardening completed
- packaged validation documented and verified

### Added

- checked-in PyInstaller spec file
- PowerShell and batch build scripts
- packaged-app validation guide
- frozen-mode settings coverage in automated tests

### Changed

- frozen-mode path resolution now prefers Windows known folders
- packaged logging is file-only and stored under LocalAppData
- default packaged output remains user-writable and is created lazily
- release docs now describe how to distribute the full packaged folder
- packaging cleanup removes transient metadata folders from the final bundle

### Validation At This Version

- copied-release-folder packaged startup smoke
- packaged real conversion smoke with explicit output path
- packaged real conversion smoke with default output path
- no new `conhost.exe` observed during packaged GUI launch
- automated unit tests and compile check

### Known Limits At This Version

- packaged release artifact is still `onedir`, not an installer
- executable signing and richer Windows metadata are still pending

## v0.1.0 - 2026-04-12 - Initial Working Foundation

Release status:

- first runnable open-source foundation
- local Windows desktop app
- real end-to-end conversion pipeline

### Added

- working desktop UI for selecting one or more PDFs and an output folder
- drag-and-drop support with selected-file list
- local PDF ingestion with native-text extraction and selective OCR routing
- page classification for summaries, line-item pages, geometry pages, and common sample/guide pages
- structured extractors for metadata, totals, line items, and roof measurements
- canonical estimate model and merge layer
- deterministic XACTDOC-style XML writer
- standards-based `.esx` zip package generation with `XACTDOC.XML`, `canonical_estimate.json`, and `manifest.json`
- export package validation
- runtime logging and user-facing validation/error states
- initial automated tests for writer validation, conversion rejection cases, and deterministic output naming
- implementation docs in `docs/`
- long-term documentation foundation in `docs_repo/`
- repeatable PyInstaller packaging with `PDF-TO-ESX-Agent.spec` and Windows build scripts

### Changed During Hardening

- improved parsing reliability for mixed packets and Allstate/State Farm guide-page layouts
- improved error handling for broken PDFs, empty parses, and invalid output paths
- improved success and warning clarity in the UI
- improved logging consistency across conversion, parsing, OCR, and export stages
- made merged output naming deterministic regardless of file-selection order
- added frozen-mode settings for packaged logs and user output folders

### Validation At This Version

- automated unit tests
- compile check
- clean-environment reinstall and UI startup smoke
- packaged executable build and startup/conversion smoke
- real conversion validation across multiple estimate-PDF layouts from the source-agent fixture set

### Known Limits At This Version

- standards-based `.esx` packaging only, not native proprietary `XACTDOC.ZIPXML`
- parser coverage is heuristic rather than universal
- OCR-heavy layouts remain the weakest extraction area
- packaged release artifact is `onedir`, not an installer
