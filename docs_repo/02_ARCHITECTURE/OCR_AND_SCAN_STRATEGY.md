# OCR And Scan Strategy

## Why This Needs Its Own Document

Scan handling is one of the main reasons estimate-PDF conversion becomes unreliable. The current app does not treat OCR as a generic fallback for everything. It uses OCR selectively, and that decision affects parsing quality directly.

## Main Components

| Component | File | Responsibility |
| --- | --- | --- |
| scan assessment | `src/pdf_to_esx_agent/parsing/document_loader.py` | decide whether a page should be routed into OCR |
| OCR runtime | `src/pdf_to_esx_agent/ocr/rapid_ocr.py` | render pages and extract OCR text locally |
| page-role selection | `src/pdf_to_esx_agent/parsing/page_classifier.py` | keep weak or non-claim pages from polluting downstream parsing |

## Current Strategy

1. Extract native PDF text first.
2. Score each page for scan-pipeline routing.
3. If OCR is available, OCR only the routed pages.
4. Prefer OCR output only when it appears materially better than the embedded text.
5. Preserve page-level provenance for downstream warnings and output metadata.

## Why Not OCR Everything

- native text is often better than OCR on already-readable PDFs
- full-document OCR is slower
- OCR can damage table alignment or collapse text when native extraction was already good enough

## What Makes A Page OCR-Worthy Today

- very low embedded text count
- very low line count
- fragmented summary or table text
- image-backed pages with weak text
- entire document has no readable text and OCR is available

## Important Current Limits

- OCR-heavy tables remain the weakest line-item case
- OCR may recover enough text for totals but still miss names or addresses
- local OCR quality depends heavily on source scan quality

## Contributor Guidance

If you are improving OCR behavior:

- start with `document_loader.py`
- avoid global OCR-on-every-page changes unless you can prove they help more than they hurt
- inspect both `*.canonical.json` and warnings after changes
- add regression coverage for the specific scan behavior you are improving

## Related Docs

- [PDF_INGESTION_FLOW.md](./PDF_INGESTION_FLOW.md)
- [PARSING_PIPELINE.md](./PARSING_PIPELINE.md)
- [../05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md](../05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md)
