# Data Flow End To End

## End-To-End Path

1. The user selects PDF files and an output folder in the desktop UI.
2. `ConversionService` validates those paths.
3. Each PDF is loaded into a `LoadedDocument`.
4. The parser converts each `LoadedDocument` into `ParsedEstimateDocument`.
5. The merger builds one `CanonicalEstimate`.
6. The exporter generates XML, JSON, and `.esx` package artifacts.
7. The validator confirms the package structure.
8. The UI shows the result and the output paths.

## Detailed Flow With Files

| Stage | Main code |
| --- | --- |
| UI input | `ui/main_window.py` |
| startup/bootstrap | `run_app.py`, `app/bootstrap.py` |
| input validation and orchestration | `core/conversion_service.py` |
| PDF load and OCR routing | `parsing/document_loader.py`, `ocr/rapid_ocr.py` |
| page-role selection | `parsing/page_classifier.py` |
| metadata/totals/items/measurements | `extract/*.py` |
| canonical merge | `core/merge.py` |
| output naming | `core/text.py` |
| XML/package write | `export/esx_writer.py` |
| structure validation | `export/validator.py` |

## Important Failure Gates

The flow intentionally stops before export when:

- a selected path does not exist
- a selected input is not a PDF
- the output path is a file instead of a directory
- a PDF yields no readable pages
- parsing yields no line items and no usable totals
- generated XML or package structure fails validation

## Why This Flow Is Useful

Every stage produces a narrower, more structured output than the previous stage. That makes failures easier to isolate and future changes easier to reason about.

## Read Next

- [MERGE_AND_RECONCILIATION.md](./MERGE_AND_RECONCILIATION.md)
- [../05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md](../05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md)
