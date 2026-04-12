# Codebase Tour

## Top-Level Layout

| Path | Role | Read next |
| --- | --- | --- |
| `run_app.py` | repo-root launcher | `app/bootstrap.py` |
| `scripts/` | launch and verification helpers | `DEVELOPMENT_SETUP.md` |
| `src/pdf_to_esx_agent/app/` | startup/bootstrap wiring | `../02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md` |
| `src/pdf_to_esx_agent/core/` | orchestration and shared utilities | `../02_ARCHITECTURE/DATA_FLOW_END_TO_END.md` |
| `src/pdf_to_esx_agent/parsing/` | PDF loading, OCR routing, page classification | `../02_ARCHITECTURE/PDF_INGESTION_FLOW.md` |
| `src/pdf_to_esx_agent/extract/` | metadata, totals, line items, measurements | `../02_ARCHITECTURE/PARSING_PIPELINE.md` |
| `src/pdf_to_esx_agent/models/` | canonical data model | `../02_ARCHITECTURE/CANONICAL_MODEL.md` |
| `src/pdf_to_esx_agent/export/` | XML/package writer and validator | `../02_ARCHITECTURE/ESX_GENERATION_FLOW.md` |
| `src/pdf_to_esx_agent/ui/` | desktop user interface | `../02_ARCHITECTURE/UI_ARCHITECTURE.md` |
| `tests/` | automated tests | `../05_TESTING_AND_DEBUG/TESTING_STRATEGY.md` |

## Best Entry Points For Reading

1. `run_app.py`
2. `src/pdf_to_esx_agent/app/bootstrap.py`
3. `src/pdf_to_esx_agent/core/conversion_service.py`
4. `src/pdf_to_esx_agent/extract/estimate_parser.py`
5. `src/pdf_to_esx_agent/core/merge.py`
6. `src/pdf_to_esx_agent/export/esx_writer.py`
7. `src/pdf_to_esx_agent/ui/main_window.py`

## Subsystem Entry Points

| Subsystem | Main entry file |
| --- | --- |
| UI | `ui/main_window.py` |
| conversion orchestration | `core/conversion_service.py` |
| PDF ingestion | `parsing/document_loader.py` |
| OCR runtime | `ocr/rapid_ocr.py` |
| page classification | `parsing/page_classifier.py` |
| structured parser | `extract/estimate_parser.py` |
| canonical merge | `core/merge.py` |
| export writer | `export/esx_writer.py` |
| export validation | `export/validator.py` |

## If You Are Debugging A Specific Problem

| Problem area | Best file to start with |
| --- | --- |
| bad file rejection | `core/conversion_service.py` |
| OCR/path-to-text issues | `parsing/document_loader.py`, `ocr/rapid_ocr.py` |
| page-role mistakes | `parsing/page_classifier.py` |
| metadata misses | `extract/metadata.py` |
| detail-line issues | `extract/line_items.py` |
| totals mismatch | `extract/totals.py`, `core/merge.py` |
| XML/package issues | `export/esx_writer.py`, `export/validator.py` |
| UI behavior | `ui/main_window.py` |

## Read Next

- [HOW_TO_ADD_NEW_PARSERS.md](./HOW_TO_ADD_NEW_PARSERS.md)
- [HOW_TO_IMPROVE_ESX_OUTPUT.md](./HOW_TO_IMPROVE_ESX_OUTPUT.md)
