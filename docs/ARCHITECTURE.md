# Architecture

## Overview

The app is organized around one strict pipeline:

`PDF files -> document loading/OCR -> structured extraction -> canonical estimate -> ESX/XML export`

That split is intentional. PDF parsing is noisy and carrier-specific. The canonical model keeps the export layer isolated from raw parser heuristics.

## Runtime Flow

1. The desktop UI collects one or more PDF paths and an output folder.
2. `ConversionService` validates the file list and drives the conversion stages.
3. `DocumentLoader` extracts native PDF text, evaluates each page, and routes text-poor/image-backed pages through OCR when available.
4. `EstimatePdfParser` runs deterministic extractors for:
   - claim and property metadata
   - summary totals
   - estimate line items
   - roof measurements
5. `EstimateMerger` merges one or more parsed documents into a single canonical estimate.
6. `EsxWriter` serializes that canonical estimate into:
   - `XACTDOC.XML`
   - `*.esx` zip package
   - `*.canonical.json`
7. `ExportPackageValidator` verifies the XML structure, package contents, and summary-reference integrity before success is returned to the UI.
8. The UI shows preview data, validation messages, status logs, and the generated output path.

## Module Boundaries

### `src/pdf_to_esx_agent/ui`

Operator-facing desktop app built with Tk/TkinterDnD2.

Responsibilities:

- drag-and-drop and file picker
- selected file list
- output folder selection
- background conversion thread
- progress/status log
- validation/error panel
- estimate preview

### `src/pdf_to_esx_agent/parsing`

Low-level document ingestion.

Responsibilities:

- open PDFs
- extract embedded text
- detect scanned or degraded pages
- run OCR on routed pages
- preserve page-level provenance such as OCR usage and scan classification
- classify pages by role

### `src/pdf_to_esx_agent/extract`

Structured estimate parsing.

Responsibilities:

- parse metadata and parties
- parse totals from summary pages
- parse line items from detail pages
- infer roofing measurements
- return one `ParsedEstimateDocument` per PDF

### `src/pdf_to_esx_agent/models`

Canonical dataclasses shared by parser, merger, UI, and exporter.

Core objects:

- `SourceDocument`
- `EstimateMetadata`
- `EstimateTotals`
- `RoofMeasurements`
- `EstimateLineItem`
- `ParsedEstimateDocument`
- `CanonicalEstimate`

### `src/pdf_to_esx_agent/core`

Cross-cutting orchestration and utilities.

Responsibilities:

- settings
- structured logging
- numeric and text normalization
- parsed-document merge logic
- end-to-end conversion service

### `src/pdf_to_esx_agent/export`

Deterministic export builder.

Responsibilities:

- build XACTDOC-style XML from the canonical model
- validate XML before save
- validate packaged `.esx` structure after save
- package XML and canonical JSON into a `.esx` zip artifact

## Canonical Merge Rules

The merger uses conservative best-effort rules:

- metadata picks the most complete non-empty value and warns on important conflicts
- line items are sorted deterministically and deduplicated on a stable content key
- totals prefer extracted summary totals, with computed line-item totals used as fallback and for validation
- roof measurements keep the largest extracted value when multiple PDFs disagree

## Logging Strategy

Logging is file-first and troubleshooting-oriented.

Logged events include:

- PDF load start
- scan/native detection
- OCR routing and usage
- parsed line-item counts
- parsed totals
- canonical merge completion
- export file paths
- exceptions and stack traces

## Why The Exporter Is Separate

Real ESX fixtures showed that native `.esx` files can contain a proprietary `XACTDOC.ZIPXML` payload. This repo does not have a native writer for that packed format.

The exporter therefore writes standards-based `XACTDOC.XML` plus a zip package wrapper. Keeping this isolated means a native packer can be added later without touching:

- PDF ingestion
- OCR
- parsing heuristics
- canonical normalization
- desktop UI

## Practical Extension Points

The safest places to extend the app are:

- `extract/line_items.py`
  Add more carrier/table patterns or code inference rules
- `extract/totals.py`
  Improve multi-coverage summary reconciliation
- `extract/metadata.py`
  Add carrier-specific metadata/date patterns
- `export/esx_writer.py`
  Replace the current package layout with a native ESX writer later
