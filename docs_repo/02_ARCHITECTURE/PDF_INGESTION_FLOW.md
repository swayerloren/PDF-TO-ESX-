# PDF Ingestion Flow

## Purpose

This document covers the path from raw PDF bytes to `LoadedDocument`, which is the parser-facing representation of an input file.

For the OCR policy details, also read [OCR_AND_SCAN_STRATEGY.md](./OCR_AND_SCAN_STRATEGY.md).

## Entry Point

PDF ingestion begins in `ConversionService.convert()`, which normalizes the selected file paths and hands each PDF to `EstimatePdfParser.parse_path()`.

`EstimatePdfParser` then calls `DocumentLoader.load_pdf_bytes()`.

## Low-Level Loading

`DocumentLoader.load_pdf_bytes()` handles:

1. opening the PDF with `pypdf`
2. extracting embedded text per page
3. counting images on each page
4. normalizing page text and lines
5. scoring whether a page should be routed into the scan pipeline

## What The Loader Produces Per Page

Each page becomes a `DocumentPage` with:

- page number
- normalized text
- normalized lines
- whether OCR was used
- text source
- scan classification
- OCR quality/provenance fields when available

## Document-Level Signals

The final `LoadedDocument` includes:

- `page_count`
- `readable_page_count`
- `extracted_text_char_count`
- `scan_classification`
- `ocr_attempted`
- `ocr_used`
- `routed_page_count`
- `ocr_page_count`
- `scan_pipeline_status`

These signals matter later for warnings, validation, and UI summaries.

## Failure Behavior

The ingestion stage can still return a `LoadedDocument` even when parsing is weak. That is intentional. Fatal conversion failure happens later in `ConversionService` if the document remains unreadable or unusable after parsing.

## Related Docs

- [OCR_AND_SCAN_STRATEGY.md](./OCR_AND_SCAN_STRATEGY.md)
- [PARSING_PIPELINE.md](./PARSING_PIPELINE.md)
- [../05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md](../05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md)
