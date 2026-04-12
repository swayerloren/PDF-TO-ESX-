# Project Overview

## Summary

`PDF TO ESX AGENT` is a local Windows desktop application that converts insurance estimate PDFs into structured export artifacts:

- `*.esx`
- `*.esx.xml`
- `*.canonical.json`

The core workflow is:

`PDFs -> text/OCR ingestion -> structured parsing -> canonical normalization -> ESX/XML generation -> package validation`

## What The App Does Today

- accepts one or more PDF files through a Tk desktop UI
- supports drag-and-drop and file picker selection
- detects whether pages are mostly native text, mixed, or scanned
- applies OCR selectively when pages appear text-poor
- parses metadata, totals, line items, and roof measurements
- merges multiple PDFs into one canonical estimate when needed
- validates generated XML and the final `.esx` package
- writes readable logs and validation messages for troubleshooting

## What The App Does Not Do

- it does not call cloud OCR or remote parsing APIs
- it does not write the proprietary Xactimate `XACTDOC.ZIPXML` format
- it does not guarantee perfect extraction for every carrier layout
- it is not packaged yet as a standalone `.exe` installer

## Main Runtime Entry Points

| Purpose | File |
| --- | --- |
| repo-root launcher | `run_app.py` |
| app bootstrap | `src/pdf_to_esx_agent/app/bootstrap.py` |
| desktop UI | `src/pdf_to_esx_agent/ui/main_window.py` |
| conversion orchestration | `src/pdf_to_esx_agent/core/conversion_service.py` |

## Main Technical Boundary

The most important boundary in the codebase is the canonical estimate model in `src/pdf_to_esx_agent/models/estimate.py`.

The parser does not write XML directly. The exporter does not parse PDFs directly. That separation is deliberate and drives most of the architecture.

## Current State

The app is currently at an initial working foundation stage:

- end-to-end conversion works
- structure validation is built in
- parser coverage is meaningful but incomplete
- documentation now exists to help external contributors extend the project safely

For version-level detail, read [../07_PROJECT_HISTORY/CHANGELOG.md](../07_PROJECT_HISTORY/CHANGELOG.md).
