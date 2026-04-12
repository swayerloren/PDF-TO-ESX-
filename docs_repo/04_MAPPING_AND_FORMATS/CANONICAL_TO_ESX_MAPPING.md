# Canonical To ESX Mapping

## Export Principle

The exporter consumes `CanonicalEstimate`, not raw parser objects.

This document is the open-source handoff view of the mapping. For the original implementation-oriented mapping, also see `docs/ESX_MAPPING.md`.

## Package-Level Outputs

| Canonical output | File |
| --- | --- |
| XML serialization | `XACTDOC.XML` and `*.esx.xml` |
| canonical serialization | `canonical_estimate.json` and `*.canonical.json` |
| package metadata | `manifest.json` |

## Top-Level XML Mapping

| Canonical area | XML section |
| --- | --- |
| estimate metadata | `PROJECT_INFO`, `CLAIM_INFO`, `CONTACTS` |
| line items | `GROUP`, `EMBEDDED_PL/SUMITEMS` |
| totals | `TOTALS` |
| roof measurements | `ROOF_MEASUREMENTS` |
| source-document provenance | `SOURCE_DOCUMENTS` |
| warnings | `VALIDATION` |

## Key Mapping Rules

- missing fields are omitted instead of filled with fake placeholders
- monetary values are normalized to two decimals
- line items are exported twice: once as readable grouped items and once as compact `SUMITEM` records
- every grouped item gets a `SUMMARY_REF` that must resolve to a `SUMITEM/@id`

## Specific Highlights

| Canonical field | XML target |
| --- | --- |
| `metadata.estimate_name` | `PROJECT_INFO/PROJECT_NAME` |
| `metadata.claim_number` | `CLAIM_INFO/CLAIM_NUMBER` |
| `metadata.property_address` | `CLAIM_INFO/PROPERTY_ADDRESS` |
| `line_items[*].description` | `GROUP/ITEMS/ITEM/DESCRIPTION`, `SUMITEM/@desc` |
| `line_items[*].replacement_cost` | `SUMITEM/@rcv` |
| `totals.replacement_cost_value` | `TOTALS/REPLACEMENT_COST_VALUE` |
| `roof.squares` | `ROOF_MEASUREMENTS/SQUARES` |
| `warnings[*]` | `VALIDATION/MESSAGE` |
| `source_documents[*]` | `SOURCE_DOCUMENTS/DOCUMENT` |

## Validation Expectations

The current writer expects the XML to contain:

- required top-level sections
- valid summary references
- parsable JSON companions
- matching XML payload inside the package

If those expectations fail, export fails before the UI reports success.
