# Public Release Notes Draft

## PDF TO ESX AGENT v0.1.0

`PDF TO ESX AGENT` is a Windows desktop application that converts one or more insurance estimate PDFs into structured ESX-style export artifacts using a local, inspectable pipeline.

## What The Project Does

The app:

- accepts estimate PDFs through a desktop UI
- detects text-heavy versus scan-heavy pages
- applies local OCR when useful
- extracts estimate metadata, totals, line items, and roof-related measurements
- normalizes that information into a canonical estimate model
- generates deterministic XML and `.esx` package outputs

## Who It Helps

This project is most useful for:

- developers building local estimate-processing workflows
- teams experimenting with PDF-to-structured-data conversion
- contributors who want to improve parsing coverage for real carrier layouts
- people who need transparent, inspectable output rather than a black-box service

## Current Scope

This first public release is a strong foundation, not a finished compatibility layer.

Current strengths:

- real runnable app
- modular parser/canonical/export architecture
- deterministic output
- clear logs, warnings, and failure messages
- strong project documentation for contributors

## What Is Still Early

- parser coverage is heuristic rather than universal
- scanned and OCR-heavy layouts remain the weakest cases
- `.esx` output is standards-based, not a proven native proprietary `XACTDOC.ZIPXML` writer
- the project does not yet ship as a packaged installer or standalone `.exe`

## Best First Contribution Areas

- broader fixture-driven parser tests
- OCR-heavy extraction improvements
- merge and totals reconciliation refinements
- stronger ESX compatibility evidence
- documentation updates tied to real behavior changes

## Read More

- [README.md](README.md)
- [ROADMAP.md](ROADMAP.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [docs_repo/](docs_repo/)
