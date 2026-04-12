# Estimate Data Model Reference

## Core Dataclasses

All core estimate dataclasses live in `src/pdf_to_esx_agent/models/estimate.py`.

## `SourceDocument`

Tracks input provenance:

- file name and path
- page counts
- extracted text counts
- scan classification
- OCR attempted/used flags
- OCR page count
- source warnings

## `EstimateMetadata`

Tracks high-level claim/estimate identity:

- estimate name, number, and date
- carrier
- insured
- property address and city/state/postal code
- claim and policy numbers
- loss/inspection dates
- estimator contact details
- price list metadata

## `EstimateTotals`

Tracks financial summary values:

- RCV
- ACV and gross ACV
- deductible
- depreciation values
- prior payments
- net payable
- tax, subtotal, line-item total, and grand total
- overhead and profit

## `RoofMeasurements`

Tracks roof-related geometry fields such as:

- surface area
- squares
- perimeter
- ridge/hip/valley
- drip edge
- starter
- felt

## `EstimateLineItem`

Tracks one normalized line item:

- source file and page
- item and category codes
- section and coverage
- description
- quantity and unit
- price, tax, RCV, depreciation, ACV
- notes
- confidence

## `ParsedEstimateDocument`

Represents one parsed PDF before merge:

- one `SourceDocument`
- metadata
- totals
- roof measurements
- line items
- warnings

## `CanonicalEstimate`

Represents the merged normalized estimate:

- creation timestamp
- merged source file names
- metadata
- totals
- roof measurements
- line items
- source documents
- warnings
- debug notes

This is the exporter input contract.
