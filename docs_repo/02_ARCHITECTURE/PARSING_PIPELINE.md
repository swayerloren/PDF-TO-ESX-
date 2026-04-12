# Parsing Pipeline

## Main Parser Entry

`EstimatePdfParser.parse_path()` is the structured parsing entry point for one PDF.

It takes the `LoadedDocument` from the ingestion layer and runs four extractors:

- `MetadataExtractor`
- `LineItemExtractor`
- `TotalsExtractor`
- `MeasurementsExtractor`

## Page Classification Before Parsing

`PageClassifier` determines which pages are likely to be:

- claim headers
- summaries
- line item pages
- geometry pages
- payment letters
- sample or explanation pages

This matters because the parser should not treat guide pages as real estimate data.

## Metadata Extraction

`extract/metadata.py` focuses on carrier, insured, property address, claim/policy identifiers, dates, estimator contact details, and price list identifiers. It uses labeled-value extraction, regex matching, and validator functions to reject obvious false positives.

## Line Item Extraction

`extract/line_items.py` parses line items buffer-by-buffer from detail pages. It detects item starts, tracks section headers, identifies quantity/unit columns, infers financial columns from token position and expected totals, and infers codes for common roofing-related patterns.

This is the most heuristic part of the parser and the highest-value area for future improvements.

## Totals Extraction

`extract/totals.py` searches summary-style pages for labeled amounts such as replacement cost value, actual cash value, depreciation, deductible, prior payments, and net payable. It falls back to line-item-derived totals when stronger summary values are missing.

## Roof Measurements

`extract/measurements.py` combines explicit geometry-page values with roof-related line-item quantities so the canonical estimate can preserve roof measurements even when one source is incomplete.

## Parser Output

The parser returns `ParsedEstimateDocument`, which contains source document metadata, extracted fields, line items, measurements, totals, and warnings.
