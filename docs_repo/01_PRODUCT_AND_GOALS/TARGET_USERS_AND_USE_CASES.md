# Target Users And Use Cases

## Primary Users

- developers who need a local, inspectable PDF-to-estimate conversion pipeline
- contractors or estimate operators who need a desktop tool instead of a web integration
- technical teams evaluating ESX-style export generation from PDFs

## Secondary Users

- open-source contributors improving parser quality
- QA reviewers validating behavior across carrier layouts
- integration developers who need canonical estimate JSON as an intermediate artifact

## Main Use Cases

### Single Estimate Conversion

Upload one estimate PDF, choose an output folder, convert, review warnings, and inspect the resulting `.esx`, `.esx.xml`, and `.canonical.json`.

### Multi-PDF Merge

Upload multiple related PDFs when one packet is split across files. The merger selects the most useful metadata, deduplicates line items, and writes one canonical/export result.

### Parser Tuning

Use real PDFs, validation messages, the canonical JSON, and the XML output to improve parsing logic for a carrier or layout.

### Export Research

Use the canonical model and XML writer as an open reference point for future ESX compatibility work.

## Non-Goals For Now

- claim lifecycle management
- cloud synchronization
- user accounts or multi-user collaboration
- automated writeback into third-party systems
