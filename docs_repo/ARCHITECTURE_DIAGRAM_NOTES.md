# Architecture Diagram Notes

## Purpose

This document explains how to draw or review architecture diagrams for `PDF TO ESX AGENT` without misrepresenting the codebase.

## The Main Diagram To Draw

The most truthful high-level diagram is:

`Desktop UI -> ConversionService -> DocumentLoader/OCR -> Extractors -> EstimateMerger -> EsxWriter -> ExportPackageValidator -> Output Artifacts`

## Components That Should Appear

| Component | Include in diagrams? | Why |
| --- | --- | --- |
| desktop UI | yes | it is the operator entry point |
| conversion orchestration | yes | it is the main runtime controller |
| document loading | yes | it is distinct from extraction |
| OCR | yes | it is a major conditional subsystem |
| page classification | yes | it materially affects what gets parsed |
| structured extractors | yes | metadata/totals/items/measurements are intentionally separate |
| canonical merge | yes | it is the key internal contract boundary |
| XML/package writer | yes | export is intentionally isolated |
| package validation | yes | success depends on post-write validation |

## Diagram Legend To Keep Consistent

Use these meanings when drawing boxes and arrows:

| Diagram element | Meaning |
| --- | --- |
| solid box | concrete runtime subsystem in the current codebase |
| dashed box | conditional or optional stage, such as OCR on text-poor pages |
| solid arrow | primary runtime control flow |
| dotted arrow | data contract passed between subsystems |
| warning badge | a stage that can add validation messages without failing immediately |

## Boundaries The Diagram Should Emphasize

- PDF ingestion is separate from parsing
- parsing is separate from canonical normalization
- canonical normalization is separate from export
- export is separate from the UI

## Things A Diagram Should Not Imply

- the UI writes XML directly
- OCR runs on every page
- parser heuristics and XML generation are one subsystem
- the current `.esx` package is a guaranteed native proprietary Xactimate export

## Useful Secondary Diagrams

### Data-Contract Diagram

Show:

- `LoadedDocument`
- `ParsedEstimateDocument`
- `CanonicalEstimate`
- `ExportPaths`

### Parser Subsystem Diagram

Show:

- `DocumentLoader`
- `PageClassifier`
- `MetadataExtractor`
- `LineItemExtractor`
- `TotalsExtractor`
- `MeasurementsExtractor`

### Export Subsystem Diagram

Show:

- `EsxWriter`
- `ExportPackageValidator`
- output files

## Related Docs

- [./02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](./02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
- [./02_ARCHITECTURE/DATA_FLOW_END_TO_END.md](./02_ARCHITECTURE/DATA_FLOW_END_TO_END.md)
- [./02_ARCHITECTURE/CANONICAL_MODEL.md](./02_ARCHITECTURE/CANONICAL_MODEL.md)
- [./02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md](./02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md)
