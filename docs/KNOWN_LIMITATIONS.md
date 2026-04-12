# Known Limitations

## ESX Packaging

- The app writes a standards-based `.esx` zip package with `XACTDOC.XML`.
- It does not write the proprietary `XACTDOC.ZIPXML` payload used by some native Xactimate ESX files.

## PDF Variability

- Insurance estimate PDFs vary significantly by carrier, adjuster platform, and scan quality.
- The parser is deterministic and local, but still heuristic. Some layouts will always need incremental tuning.

## OCR-Heavy Files

- Scanned/image-heavy PDFs can still produce collapsed words, merged address lines, or partial party names.
- OCR-heavy line-item tables are the most likely source of large summary-vs-detail mismatch warnings.
- Full-document OCR runs are slower than native-text extraction and can take noticeably longer on multi-page scans.

## Line Item Parsing

- Some carriers mix percentages, taxes, depreciation, and totals on the same visual row in inconsistent orders.
- The parser handles common patterns, but unusual column orders can still distort individual line-item totals.
- When summary totals are stronger than line-item totals, the canonical totals prefer the summary values and surface warnings instead of failing the export.

## Metadata Availability

- `estimate_number` is not always present in the source PDF and may remain blank.
- Some letter-plus-estimate bundles expose the claim and payment data clearly but do not carry a clean standalone estimate title/number.
- Scanned PDFs may provide enough information to export but still miss insured or estimator details.

## Multi-Section Documents

- Some carrier packets include instructional pages, reference guides, payment letters, and the actual estimate in the same PDF.
- The app now excludes common sample/guide pages, but other mixed-content bundles may still need page-classifier tuning.

## Totals Reconciliation

- A warning may appear when parsed line-item totals differ materially from summary totals.
- That warning does not necessarily mean export failure; it indicates that the summary section was trusted over noisy detail parsing.

## Desktop Runtime

- The app is designed for Windows + VS Code + local Python.
- It is not currently packaged as a standalone installer or `.exe`.
