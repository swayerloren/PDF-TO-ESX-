# Canonical Model

## Why A Canonical Model Exists

The parser sees messy, carrier-specific PDF content. The exporter needs stable, predictable data.

The canonical model exists to separate those concerns.

Without that boundary, the XML writer would have to understand OCR quality problems, page roles, parser fallback rules, and conflicting metadata across multiple PDFs.

## Main Canonical Types

Defined in `src/pdf_to_esx_agent/models/estimate.py`:

| Type | Purpose |
| --- | --- |
| `ValidationMessage` | warnings, errors, and info messages |
| `SourceDocument` | provenance and scan/OCR details per input file |
| `EstimateMetadata` | claim and estimate metadata |
| `EstimateTotals` | summary financial values |
| `RoofMeasurements` | roof geometry values |
| `EstimateLineItem` | normalized line item data |
| `ParsedEstimateDocument` | one parsed PDF before merge |
| `CanonicalEstimate` | final normalized estimate used for export |

## Merge Behavior

`EstimateMerger` creates `CanonicalEstimate` from one or more parsed documents.

Key rules:

- metadata prefers the most complete usable value and warns on important conflicts
- line items are sorted deterministically and deduplicated
- totals prefer the strongest summary source, with line-item totals used for fallback and validation
- roof measurements keep the largest extracted value when multiple documents disagree

## Contributor Rule

If you add parsing logic, aim to improve the canonical estimate. Do not jump straight from a new PDF pattern to XML-writing logic.

## Related Docs

- [MERGE_AND_RECONCILIATION.md](./MERGE_AND_RECONCILIATION.md)
- [../04_MAPPING_AND_FORMATS/ESTIMATE_DATA_MODEL_REFERENCE.md](../04_MAPPING_AND_FORMATS/ESTIMATE_DATA_MODEL_REFERENCE.md)
- [../06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md](../06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md)
