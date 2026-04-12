# AGENT ANALYSIS FOR PDF TO ESX

## Task Classification

The source repo analysis split into two useful lanes:

- agent-side parsing and canonical-estimate architecture under `src/services/insurance_scope`, `src/services/canonical_estimate`, and `src/services/esx`
- local desktop UI patterns under `src/platform/claim_operator_view.py` and related startup wrappers

Salesforce-specific orchestration, worker queues, runtime trust, local model management, and platform supervision were intentionally excluded from this new app.

## What Was Reusable

### 1. PDF ingestion and scan detection

Most useful source modules:

- `src/services/insurance_scope/document_loader.py`
- `src/services/insurance_scope/ocr_support.py`
- `src/services/insurance_scope/page_classifier.py`
- `AGENT HISTORY/SYSTEMS/pdf_parsing/README.md`

Reusable patterns:

- load native PDF text first
- classify pages as native, mixed, or scanned instead of assuming one mode
- route only weak or image-backed pages into OCR rather than OCRing the entire file blindly
- preserve page-level metadata such as `ocr_used`, scan classification, and text source
- treat image-only failure as an explicit extraction problem, not a silent low-confidence parse

Decision for this repo:

- keep the staged `native text -> scan detection -> optional OCR replacement` flow
- keep readable page/document metadata for preview, logs, and troubleshooting
- simplify the original OCR cache/runtime coupling so this app stays standalone

### 2. Insurance-estimate parsing structure

Most useful source modules:

- `src/agents/insurance_scope/agent.py`
- `src/services/insurance_scope/identity_extractor.py`
- `src/services/insurance_scope/summary_parser.py`
- `src/services/insurance_scope/line_item_parser.py`
- `src/services/insurance_scope/roof_geometry_parser.py`
- `AGENT HISTORY/SYSTEMS/insurance_scope_analyzer/README.md`

Reusable patterns:

- separate extraction into page classification, identity extraction, summary/totals parsing, line-item parsing, roof geometry parsing, and final reconciliation
- never trust guide/sample pages as real claim data
- preserve both claim-level totals and detail-level line items
- keep parsing heuristics deterministic and file-local
- prefer a summary-first fallback for financial totals when line-item math is incomplete

Decision for this repo:

- keep the same staged parser design
- adapt the line-item buffer parsing and section-detection approach
- reuse the claim/property/date/price-list style heuristics
- keep the implementation leaner than the source repo by removing Salesforce writeback and supplement logic

### 3. Canonical estimate boundary

Most useful source modules/docs:

- `src/services/canonical_estimate/adapters/insurance_scope.py`
- `src/services/canonical_estimate/common.py`
- `AGENT HISTORY/SYSTEMS/canonical_estimate/README.md`
- `AGENT INFO CHAT GPT.MD`

Reusable patterns:

- do not export directly from parser internals
- normalize extracted output into a source-neutral canonical estimate model first
- keep field confidence, source provenance, and notes close to the data
- make exporters consume canonical output rather than PDF parser objects

Decision for this repo:

- create a standalone canonical estimate model for PDF-derived estimates
- include source documents, metadata, line items, totals, roof measurements, validation warnings, and merge notes
- keep the schema smaller than the source repo's claim-packet model because this app only needs `PDF -> canonical -> ESX/XML`

### 4. ESX knowledge and export target

Most useful source modules/docs:

- `src/services/esx/parser.py`
- `src/services/esx/runtime.py`
- `src/services/canonical_estimate/adapters/esx.py`
- `tests/canonical/test_canonical_translation.py`

What the source repo proved:

- the machine has real `.esx` fixtures
- the inner estimate payload is real `XACTDOC` XML
- actual samples contain structures like `PROJECT_INFO`, `GROUP`, `ITEMS`, `SUMMARY_REF`, `PARAMS`, `ADM`, `CLAIM_INFO`, `CONTACTS`, and `EMBEDDED_PL`
- the outer `.esx` archive contains a proprietary `XACTDOC.ZIPXML` payload, not plain XML

Important constraint:

- the source repo has a real ESX reader through the local Xactimate runtime, but it does not include a native ESX writer/packer for `XACTDOC.ZIPXML`

Decision for this repo:

- build a deterministic XACTDOC-style XML exporter using the real sample structure as the reference
- isolate the schema builder in one module so native `.esx` packaging can be swapped in later
- document clearly that the app currently emits standards-based XACTDOC XML output modeled on real ESX content rather than the proprietary packed container

### 5. Desktop UI approach

Most useful source modules/docs:

- `src/platform/claim_operator_view.py`
- `src/run_claim_operator_view.py`
- `APP HISTORY/SYSTEMS/claim_operator_view/README.md`

Reusable patterns:

- simple Tk desktop app
- artifact-driven UI instead of hiding logic inside the view
- strong emphasis on status text, refresh actions, and readable operator workflows
- no fake controls or decorative-only surfaces

Decision for this repo:

- build a standalone desktop UI with the same general philosophy: reliable, lightweight, operator-facing, and file-driven
- keep the visual language cleaner and simpler than the claim operator view
- add drag/drop, file list, output folder selector, preview, status, and validation panels

## What Was Explicitly Left Out

These source-repo areas were not reused because they are irrelevant or too coupled to the old platform:

- Salesforce clients, run services, and file download/writeback services
- worker supervision, runtime trust, portable Python/Ollama, and background platform bootstrap
- claim-packet review gating and export-bundle orchestration
- local-model-assisted analysis paths
- packaged exe build/runtime assumptions from the old platform

## Architecture Decisions For This New Repo

The new app uses these boundaries:

1. `parsing/`
   PDF loading, scan detection, OCR, and page classification
2. `extract/`
   metadata, totals, line items, measurements, and canonical parse assembly
3. `models/`
   canonical estimate dataclasses and serialization helpers
4. `export/`
   XACTDOC-style XML generation and validation
5. `ui/`
   desktop app only
6. `core/`
   settings, logging, numeric/text helpers, and orchestration glue

## Best Reuse Summary

The source repo was most valuable as a design reference, not as a drop-in dependency. The strongest reusable ideas were:

- OCR-aware page routing instead of naive text extraction
- parser stages that stay separate and deterministic
- canonical-model boundary before export
- artifact-driven desktop UI
- real ESX structural knowledge from sample files and parser output

That is the exact subset carried into this project.

