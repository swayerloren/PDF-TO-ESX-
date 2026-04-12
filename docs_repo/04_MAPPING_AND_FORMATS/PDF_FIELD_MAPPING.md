# PDF Field Mapping

## Purpose

This document explains how the current parser maps PDF content into canonical estimate fields.

The mapping is heuristic. It describes the current implementation, not a promise that every carrier layout will behave identically.

## Metadata Mapping

| Canonical field | Main source | Current strategy |
| --- | --- | --- |
| `estimate_name` | visible title lines, labeled estimate text, file name fallback | `MetadataExtractor._estimate_name()` |
| `estimate_number` | labeled estimate number, regex fallback | `MetadataExtractor._estimate_number()` |
| `estimate_date` | labeled date values, date regex fallback | `MetadataExtractor.extract()` |
| `carrier` | full-document keyword detection | `MetadataExtractor._detect_carrier()` |
| `insured_name` | labeled insured text, “To: Name” pattern, regex fallback | `MetadataExtractor._extract_insured_name()` |
| `property_address` | labeled property/location lines, street + city/state/zip patterns | `MetadataExtractor._extract_property_address()` |
| `claim_number` | labeled values and claim-number regex | `MetadataExtractor._extract_claim_number()` |
| `policy_number` | labeled values and policy-number regex | `MetadataExtractor._extract_policy_number()` |
| `date_of_loss` | labeled date or regex fallback | `MetadataExtractor.extract()` |
| `date_inspected` | labeled date or regex fallback | `MetadataExtractor.extract()` |
| `estimator_name` | estimator/adjuster labels plus nearby-name patterns | `MetadataExtractor._extract_estimator_name()` |
| `estimator_phone` | phone regex over actual claim text | `MetadataExtractor._extract_estimator_phone()` |
| `estimator_email` | email regex over actual claim text | `MetadataExtractor._extract_estimator_email()` |
| `price_list_*` | price-list code regex and suffix split | `MetadataExtractor.extract()` |

## Totals Mapping

Totals are parsed mainly from summary pages selected by `PageClassifier.summary_pages()`.

| Canonical field | Example PDF labels | Notes |
| --- | --- | --- |
| `replacement_cost_value` | replacement cost value, replacement cost, total loss | preferred summary total |
| `actual_cash_value` | actual cash value, acv total, total acv settlement | may also feed `gross_acv` |
| `deductible` | deductible, less deductible | stored as positive number |
| `depreciation` | less depreciation, depreciation | stored as positive number |
| `recoverable_depreciation` | replacement cost benefits, recoverable depreciation | often summary-only |
| `prior_payments` | prior payment, previous payment | stored as positive number |
| `net_payable` | net actual cash value payment, amount payable | summary-first |
| `total_if_incurred` | total amount of claim if incurred, total paid when incurred | summary-first |
| `tax_total` | sales tax, material sales tax | summary-first, line-item fallback |
| `line_item_total` | line item total, subtotal | summary-first, line-item fallback |
| `grand_total` | grand total, total estimate | summary-first, derived fallback |

## Line Item Mapping

Line item extraction begins on pages selected by `PageClassifier.line_item_pages()`.

The extractor currently assumes:

- line items start with an item-number-like token
- one line in the buffer contains quantity and unit
- money tokens after quantity can be assigned into unit price, tax, replacement cost, depreciation, and ACV based on expected order and expected quantity * unit price math

| Canonical field | Source pattern |
| --- | --- |
| `item_number` | normalized token at the start of the line item |
| `section_name` | section header lines above item buffers |
| `description` | non-numeric text before the numeric line |
| `quantity` | `QTY_UNIT_RE` |
| `unit` | `QTY_UNIT_RE` |
| `unit_price` | first usable money token, adjusted if total math is stronger |
| `tax` | money token before detected RCV when it behaves like tax |
| `replacement_cost` | detected “RCV-like” money token |
| `depreciation` | tail money token, often percentage-adjacent |
| `actual_cash_value` | trailing money token or `RCV - depreciation` fallback |
| `item_code` and components | inferred from description/notes keywords |

## Roof Measurement Mapping

Roof measurements come from two places:

- explicit geometry pages
- line-item-derived quantities for common roofing descriptions

Examples:

- shingle squares from shingle line items in `SQ`
- felt squares from felt items
- drip edge and starter from `LF` line items
- ice and water from `SF` or `SQ`

## Fallback Behavior

When summary totals are missing, the parser tries to recover usable totals from line items. When line-item math is noisy but summary totals are stronger, the canonical estimate prefers the summary values and warns.
