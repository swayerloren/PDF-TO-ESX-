# Why This Exists

## Immediate Reason

The project was built to provide a working local bridge between real insurance estimate PDFs and structured ESX-style output.

## Why Existing Approaches Were Not Enough

- Manual re-entry is slow and error-prone.
- Closed vendor tooling is hard to inspect and extend.
- A direct parser-to-XML design becomes unmaintainable as PDF layouts vary.
- Cloud-first approaches create dependency, cost, and privacy concerns that are not necessary for the current goal.

## Why The Current Architecture Was Chosen

The app uses:

- local PDF text extraction first
- selective OCR instead of OCR-everything
- separate parser stages for metadata, totals, line items, and roof measurements
- a canonical estimate layer before export
- a replaceable ESX writer

That architecture exists because it is easier to debug, easier to extend, and safer to evolve than a single monolithic converter.

## Why SALES FORCE AGENT Matters Here

The source agent repo already contained useful patterns:

- OCR-aware document ingestion
- page classification for mixed packets
- staged estimate parsing
- canonical estimate concepts
- real ESX structure references

Those ideas were reused, but Salesforce-specific orchestration, platform runtime code, and unrelated app infrastructure were intentionally left out.
