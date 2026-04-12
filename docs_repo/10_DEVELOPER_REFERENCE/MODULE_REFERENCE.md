# Module Reference

## `app`

- `bootstrap.py`
  builds settings, logging, conversion service, and main window

## `core`

- `conversion_service.py`
  central orchestration and validation path
- `logging.py`
  root logger setup
- `merge.py`
  canonical merge logic
- `numbers.py`
  decimal helpers and numeric token parsing
- `settings.py`
  repo-relative runtime settings
- `text.py`
  text normalization and safe output naming

## `parsing`

- `document_loader.py`
  PDF loading, scan routing, OCR preference logic
- `page_classifier.py`
  claim/summary/line-item/geometry/sample-page classification

## `extract`

- `estimate_parser.py`
  top-level parser entry for one PDF
- `metadata.py`
  metadata and contact extraction
- `line_items.py`
  line-item parsing and code inference
- `totals.py`
  summary total extraction and fallback totals
- `measurements.py`
  roof geometry inference

## `models`

- `estimate.py`
  canonical dataclasses and serialization helpers

## `export`

- `esx_writer.py`
  XML and package builder
- `validator.py`
  XML/package validation rules

## `ui`

- `main_window.py`
  desktop app behavior and state presentation

## High-Value Modules For Contributors

| Goal | Main module |
| --- | --- |
| improve bad input handling | `core/conversion_service.py` |
| improve scan/text routing | `parsing/document_loader.py` |
| improve layout detection | `parsing/page_classifier.py` |
| improve line-item accuracy | `extract/line_items.py` |
| improve totals quality | `extract/totals.py` |
| improve multi-file behavior | `core/merge.py` |
| improve export compatibility | `export/esx_writer.py`, `export/validator.py` |

## Read Next

- [./FILE_AND_FOLDER_REFERENCE.md](./FILE_AND_FOLDER_REFERENCE.md)
- [../02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](../02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
- [../06_CONTRIBUTING/CODEBASE_TOUR.md](../06_CONTRIBUTING/CODEBASE_TOUR.md)
