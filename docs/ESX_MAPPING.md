# ESX Mapping

## Export Shape

The app generates:

- `*.esx`
  Zip package containing `XACTDOC.XML`, `canonical_estimate.json`, and `manifest.json`
- `*.esx.xml`
  The same XML payload written as a standalone file for inspection

The XML root is `XACTDOC`, based on structures observed in real ESX fixtures from the source agent repo.

## Mapping Principles

- parse PDFs into a canonical estimate first
- export from the canonical model only
- keep XML deterministic
- omit empty fields instead of writing fake placeholders
- escape text through XML serialization, not string concatenation
- keep package validation separate from parsing heuristics

## Package-Level Mapping

| Source | Output |
| --- | --- |
| canonical estimate | `XACTDOC.XML` |
| canonical estimate JSON serialization | `canonical_estimate.json` |
| package metadata | `manifest.json` |

## Root Attributes

| Canonical source | XML target |
| --- | --- |
| fixed export name | `XACTDOC/@generatedBy` |
| writer schema version | `XACTDOC/@schemaVersion` |
| `CanonicalEstimate.created_at` | `XACTDOC/@createdAt` |

## Project Info

| Canonical field | XML target |
| --- | --- |
| `metadata.estimate_name` | `PROJECT_INFO/PROJECT_NAME` |
| `metadata.estimate_number` | `PROJECT_INFO/ESTIMATE_NUMBER` |
| `metadata.estimate_date` | `PROJECT_INFO/ESTIMATE_DATE` |
| `metadata.price_list_code` | `PROJECT_INFO/PRICE_LIST_CODE` |
| `metadata.price_list_region` | `PROJECT_INFO/PRICE_LIST_REGION` |
| `metadata.price_list_month` | `PROJECT_INFO/PRICE_LIST_MONTH` |
| `metadata.price_list_year` | `PROJECT_INFO/PRICE_LIST_YEAR` |
| `merged_from_files` | `PROJECT_INFO/MERGED_FROM_FILES` |

## Claim Info

| Canonical field | XML target |
| --- | --- |
| `metadata.carrier` | `CLAIM_INFO/CARRIER` |
| `metadata.claim_number` | `CLAIM_INFO/CLAIM_NUMBER` |
| `metadata.policy_number` | `CLAIM_INFO/POLICY_NUMBER` |
| `metadata.date_of_loss` | `CLAIM_INFO/DATE_OF_LOSS` |
| `metadata.date_inspected` | `CLAIM_INFO/DATE_INSPECTED` |
| `metadata.property_address` | `CLAIM_INFO/PROPERTY_ADDRESS` |
| `metadata.city` | `CLAIM_INFO/CITY` |
| `metadata.state` | `CLAIM_INFO/STATE` |
| `metadata.postal_code` | `CLAIM_INFO/POSTAL_CODE` |

## Contacts

| Canonical field | XML target |
| --- | --- |
| `metadata.insured_name` | `CONTACTS/CONTACT[@role='insured']/NAME` |
| `metadata.property_address` | `CONTACTS/CONTACT[@role='insured']/ADDRESS` |
| `metadata.estimator_name` | `CONTACTS/CONTACT[@role='estimator']/NAME` |
| `metadata.estimator_phone` | `CONTACTS/CONTACT[@role='estimator']/PHONE` |
| `metadata.estimator_email` | `CONTACTS/CONTACT[@role='estimator']/EMAIL` |

## Price List / Embedded PL

| Canonical field | XML target |
| --- | --- |
| `metadata.price_list_code` | `EMBEDDED_PL/PRICE_LIST/@code` |
| `metadata.price_list_region` | `EMBEDDED_PL/PRICE_LIST/@region` |
| `metadata.price_list_month` | `EMBEDDED_PL/PRICE_LIST/@month` |
| `metadata.price_list_year` | `EMBEDDED_PL/PRICE_LIST/@year` |

## Line Item Mapping

Each canonical line item is exported twice:

1. `GROUP/ITEMS/ITEM`
   Human-readable grouping record with source file, page, section, coverage, notes, and a `SUMMARY_REF`
2. `EMBEDDED_PL/SUMITEMS/SUMITEM`
   Compact ESX-style record used by the package payload

### `GROUP/ITEMS/ITEM`

| Canonical field | XML target |
| --- | --- |
| array position | `ITEM/@id` |
| `source_file` | `ITEM/@sourceFile` |
| `page_number` | `ITEM/@page` |
| `item_number` | `ITEM/ITEM_NUMBER` |
| `section_name` | `ITEM/SECTION` |
| `coverage_name` | `ITEM/COVERAGE` |
| `description` | `ITEM/DESCRIPTION` |
| generated summary id | `ITEM/SUMMARY_REF/@ref` |
| `notes[*]` | repeated `ITEM/NOTE` |

### `EMBEDDED_PL/SUMITEMS/SUMITEM`

| Canonical field | XML target |
| --- | --- |
| array position | `SUMITEM/@id`, `SUMITEM/@seq` |
| `category_code` | `SUMITEM/@cat` |
| `selector_code` | `SUMITEM/@sel` |
| `activity_code` | `SUMITEM/@act` |
| `item_code` | `SUMITEM/@code` |
| `description` | `SUMITEM/@desc` |
| `unit` | `SUMITEM/@unit` |
| `quantity` | `SUMITEM/@qty` |
| `unit_price` | `SUMITEM/@price` |
| `tax` | `SUMITEM/@tax` |
| `replacement_cost` | `SUMITEM/@rcv` |
| `depreciation` | `SUMITEM/@dep` |
| `actual_cash_value` | `SUMITEM/@acv` |
| `overhead_and_profit` | `SUMITEM/@op` |
| `section_name` | `SUMITEM/@section` |
| `coverage_name` | `SUMITEM/@coverage` |
| `confidence` | `SUMITEM/@confidence` |
| `notes[*]` | repeated `SUMITEM/NOTE` |

## Totals Mapping

| Canonical field | XML target |
| --- | --- |
| `replacement_cost_value` | `TOTALS/REPLACEMENT_COST_VALUE` |
| `actual_cash_value` | `TOTALS/ACTUAL_CASH_VALUE` |
| `gross_acv` | `TOTALS/GROSS_ACV` |
| `deductible` | `TOTALS/DEDUCTIBLE` |
| `depreciation` | `TOTALS/DEPRECIATION` |
| `recoverable_depreciation` | `TOTALS/RECOVERABLE_DEPRECIATION` |
| `nonrecoverable_depreciation` | `TOTALS/NONRECOVERABLE_DEPRECIATION` |
| `prior_payments` | `TOTALS/PRIOR_PAYMENTS` |
| `net_payable` | `TOTALS/NET_PAYABLE` |
| `total_if_incurred` | `TOTALS/TOTAL_IF_INCURRED` |
| `tax_total` | `TOTALS/TAX_TOTAL` |
| `subtotal` | `TOTALS/SUBTOTAL` |
| `overhead_and_profit` | `TOTALS/OVERHEAD_AND_PROFIT` |
| `line_item_total` | `TOTALS/LINE_ITEM_TOTAL` |
| `grand_total` | `TOTALS/GRAND_TOTAL` |

## Roof Measurement Mapping

| Canonical field | XML target |
| --- | --- |
| `surface_area_sq_ft` | `ROOF_MEASUREMENTS/SURFACE_AREA_SQ_FT` |
| `squares` | `ROOF_MEASUREMENTS/SQUARES` |
| `perimeter_lf` | `ROOF_MEASUREMENTS/PERIMETER_LF` |
| `ridge_lf` | `ROOF_MEASUREMENTS/RIDGE_LF` |
| `hip_lf` | `ROOF_MEASUREMENTS/HIP_LF` |
| `valley_lf` | `ROOF_MEASUREMENTS/VALLEY_LF` |
| `eaves_lf` | `ROOF_MEASUREMENTS/EAVES_LF` |
| `rakes_lf` | `ROOF_MEASUREMENTS/RAKES_LF` |
| `drip_edge_lf` | `ROOF_MEASUREMENTS/DRIP_EDGE_LF` |
| `ice_water_sf` | `ROOF_MEASUREMENTS/ICE_WATER_SF` |
| `starter_lf` | `ROOF_MEASUREMENTS/STARTER_LF` |
| `felt_squares` | `ROOF_MEASUREMENTS/FELT_SQUARES` |

## Source Document Mapping

| Canonical field | XML target |
| --- | --- |
| `file_name` | `SOURCE_DOCUMENTS/DOCUMENT/@fileName` |
| `file_path` | `SOURCE_DOCUMENTS/DOCUMENT/@filePath` |
| `page_count` | `SOURCE_DOCUMENTS/DOCUMENT/@pageCount` |
| `readable_page_count` | `SOURCE_DOCUMENTS/DOCUMENT/@readablePageCount` |
| `scan_classification` | `SOURCE_DOCUMENTS/DOCUMENT/@scanClassification` |
| `text_source` | `SOURCE_DOCUMENTS/DOCUMENT/@textSource` |
| `ocr_attempted` | `SOURCE_DOCUMENTS/DOCUMENT/@ocrAttempted` |
| `ocr_used` | `SOURCE_DOCUMENTS/DOCUMENT/@ocrUsed` |
| `ocr_page_count` | `SOURCE_DOCUMENTS/DOCUMENT/@ocrPageCount` |
| `warnings[*]` | repeated `SOURCE_DOCUMENTS/DOCUMENT/WARNING` |

## Validation / Audit Mapping

| Canonical field | XML target |
| --- | --- |
| `warnings[*].level` | `VALIDATION/MESSAGE/@level` |
| `warnings[*].context` | `VALIDATION/MESSAGE/@context` |
| `warnings[*].message` | `VALIDATION/MESSAGE` text |
| fixed export audit entry | `AUDIT_ENTRIES/AUDIT_ENTRY` |

## XML And Package Validation

After XML generation, the app validates:

- XML is well-formed
- root tag is `XACTDOC`
- required top-level sections exist
- every `GROUP/ITEMS/ITEM/SUMMARY_REF/@ref` points to an existing `EMBEDDED_PL/SUMITEMS/SUMITEM/@id`
- the `.esx` zip contains `XACTDOC.XML`, `canonical_estimate.json`, and `manifest.json`
- packaged XML matches the standalone XML payload
- `manifest.json` and `canonical_estimate.json` parse as valid JSON

## Current Limitation

This is not a native writer for the proprietary `XACTDOC.ZIPXML` payload used inside some production ESX archives. The app instead emits an open, inspectable XML package that preserves the canonical estimate and keeps the writer replaceable later.
