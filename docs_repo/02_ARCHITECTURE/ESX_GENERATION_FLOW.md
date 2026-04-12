# ESX Generation Flow

## Purpose

This document explains how the current app turns `CanonicalEstimate` into export artifacts and where the current ESX assumptions begin and end.

## Export Entry

Export generation begins after `ConversionService` has a `CanonicalEstimate`.

The exporter lives in `src/pdf_to_esx_agent/export/esx_writer.py`.

## What The Writer Produces

For each conversion, the writer creates:

- `*.esx.xml`
- `*.canonical.json`
- `*.esx`

The `.esx` file is a zip package containing:

- `XACTDOC.XML`
- `canonical_estimate.json`
- `manifest.json`

## XML Structure

The XML root is `XACTDOC`.

Top-level sections currently include:

- `PROJECT_INFO`
- `PARAMS`
- `ADM`
- `CLAIM_INFO`
- `CONTACTS`
- `GROUP`
- `EMBEDDED_PL`
- `TOTALS`
- `ROOF_MEASUREMENTS`
- `SOURCE_DOCUMENTS`
- `VALIDATION`
- `AUDIT_ENTRIES`

## What The Exporter Assumes

- missing fields should be omitted rather than faked
- text should be escaped by XML serialization, not manual string concatenation
- monetary values should be normalized
- grouped items and `SUMITEM` records should stay linked through `SUMMARY_REF`

## Validation Step

`ExportPackageValidator` runs after XML generation and after package creation.

It checks:

- XML well-formedness
- required top-level sections
- `SUMMARY_REF` integrity
- package contents
- JSON validity inside the `.esx` archive
- package XML consistency with the standalone XML payload

The UI should only report success after this validation passes.

## High-Risk Change Area

Do not change the writer casually if the real issue is parser quality. If a field is missing in XML because it never existed in `CanonicalEstimate`, fix the parser/canonical layer first.

## Related Docs

- [CANONICAL_MODEL.md](./CANONICAL_MODEL.md)
- [../04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md](../04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md)
- [../04_MAPPING_AND_FORMATS/XML_ESX_ASSUMPTIONS.md](../04_MAPPING_AND_FORMATS/XML_ESX_ASSUMPTIONS.md)
