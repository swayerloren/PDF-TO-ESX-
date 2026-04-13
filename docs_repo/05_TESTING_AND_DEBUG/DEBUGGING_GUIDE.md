# Debugging Guide

## First Places To Look

When something goes wrong, inspect in this order:

1. the UI validation panel
2. the runtime log file
   source mode: `logs/pdf_to_esx_agent.log`
   packaged mode: `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`
3. the generated `*.canonical.json` if export succeeded with warnings
4. the generated `*.esx.xml` if XML shape looks suspicious

## Debug By Pipeline Stage

| Symptom | Likely stage |
| --- | --- |
| file rejected before work starts | `ConversionService` path validation |
| no readable text | `DocumentLoader` / OCR availability |
| missing claim/property metadata | `MetadataExtractor` |
| weak or missing detail lines | `LineItemExtractor` |
| totals mismatch warnings | `TotalsExtractor` or `EstimateMerger` |
| output package rejected | `EsxWriter` or `ExportPackageValidator` |

## Useful Artifacts

- source log: `logs/pdf_to_esx_agent.log`
- packaged log: `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`
- `*.canonical.json`
- `*.esx.xml`
- `docs/TESTING_NOTES.md`

## Practical Debug Method

1. reproduce with one PDF first
2. inspect whether the document was classified as native, mixed, or scanned
3. inspect canonical JSON before touching XML generation
4. decide whether the bug belongs to ingestion, extraction, merge, or export
5. add or update a regression test when the fix is stable

## What To Avoid

- changing export code to hide parser problems
- changing the UI to suppress meaningful warnings
- assuming OCR should replace native text everywhere
