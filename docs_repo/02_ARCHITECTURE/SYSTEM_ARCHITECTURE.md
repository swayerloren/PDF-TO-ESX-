# System Architecture

## Overview

The app is organized as a layered local pipeline:

`UI -> ConversionService -> parsing/ocr -> extractors -> canonical merge -> export -> package validation`

This is the most important architectural fact in the repo. Most contributor decisions should preserve that split.

## Architecture At A Glance

| Layer | Main files | Responsibility | Read next |
| --- | --- | --- | --- |
| UI | `ui/main_window.py` | collect files, run conversion, present status and results | [UI_ARCHITECTURE.md](./UI_ARCHITECTURE.md) |
| bootstrap | `app/bootstrap.py`, `run_app.py` | load settings, configure logging, construct services | [../10_DEVELOPER_REFERENCE/CONFIG_REFERENCE.md](../10_DEVELOPER_REFERENCE/CONFIG_REFERENCE.md) |
| orchestration | `core/conversion_service.py` | validate inputs, drive stages, surface errors | [DATA_FLOW_END_TO_END.md](./DATA_FLOW_END_TO_END.md) |
| parsing and OCR | `parsing/document_loader.py`, `parsing/page_classifier.py`, `ocr/rapid_ocr.py` | load pages, route OCR, classify page roles | [PDF_INGESTION_FLOW.md](./PDF_INGESTION_FLOW.md), [OCR_AND_SCAN_STRATEGY.md](./OCR_AND_SCAN_STRATEGY.md) |
| extraction | `extract/*.py` | parse metadata, totals, line items, measurements | [PARSING_PIPELINE.md](./PARSING_PIPELINE.md) |
| canonical model and merge | `models/estimate.py`, `core/merge.py` | normalize parsed documents into one stable estimate | [CANONICAL_MODEL.md](./CANONICAL_MODEL.md), [MERGE_AND_RECONCILIATION.md](./MERGE_AND_RECONCILIATION.md) |
| export | `export/esx_writer.py`, `export/validator.py` | build XML/package and validate structure | [ESX_GENERATION_FLOW.md](./ESX_GENERATION_FLOW.md) |

## Main Runtime Contracts

| Contract | Producer | Consumer | Why it exists |
| --- | --- | --- | --- |
| `LoadedDocument` | `DocumentLoader` | extractors | preserve page text, OCR provenance, and scan classification |
| `ParsedEstimateDocument` | `EstimatePdfParser` | `EstimateMerger` | keep one parsed-PDF result isolated before merge |
| `CanonicalEstimate` | `EstimateMerger` | `EsxWriter`, UI preview | provide a stable source-of-truth model for export |
| `ExportPaths` | `EsxWriter` | `ConversionService`, UI | return a deterministic record of generated artifacts |

## Why The Architecture Looks Like This

- PDF ingestion and OCR are noisy and input-dependent.
- extraction is heuristic and layout-sensitive.
- canonical normalization is the stability boundary.
- export assumptions may evolve independently of parsing rules.

If these concerns were collapsed into one module, debugging and contribution would become much harder.

## Architectural Invariants

- the UI should not parse PDFs directly
- the exporter should not parse raw PDF text
- parser improvements should flow through the canonical model
- output success should depend on export validation, not only file creation

## Related Docs

- [DATA_FLOW_END_TO_END.md](./DATA_FLOW_END_TO_END.md)
- [CANONICAL_MODEL.md](./CANONICAL_MODEL.md)
- [MERGE_AND_RECONCILIATION.md](./MERGE_AND_RECONCILIATION.md)
- [../ARCHITECTURE_DIAGRAM_NOTES.md](../ARCHITECTURE_DIAGRAM_NOTES.md)
