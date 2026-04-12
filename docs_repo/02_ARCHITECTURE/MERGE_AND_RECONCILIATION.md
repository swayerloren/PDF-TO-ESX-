# Merge And Reconciliation

## Why This Subsystem Exists

`PDF TO ESX AGENT` supports one or more input PDFs per conversion run.

That creates a real architectural problem: different files can contain overlapping line items, conflicting metadata, stronger summary totals, or supplemental roof information. The merge layer exists so the rest of the system does not have to solve those conflicts ad hoc.

The implementation lives in `src/pdf_to_esx_agent/core/merge.py`.

## Inputs And Output

| Type | Meaning |
| --- | --- |
| `ParsedEstimateDocument` | one parsed PDF result with metadata, totals, roof data, line items, warnings, and source provenance |
| `CanonicalEstimate` | the merged result used by the UI preview and `EsxWriter` |

## What The Merger Actually Does

`EstimateMerger.merge()`:

1. sorts parsed documents deterministically by source file name
2. carries forward warnings from individual parsed documents
3. selects the strongest metadata values across documents
4. deduplicates and enriches line items
5. reconciles totals from summary sections and line-item math
6. combines roof measurements
7. records debug notes so downstream troubleshooting has merge provenance

## Metadata Reconciliation Rules

Metadata is merged field by field, not document by document.

Current behavior:

- the merger looks at every populated candidate for each metadata field
- it prefers stronger values by simple score and by the overall completeness of the source document
- for high-value fields like claim number, policy number, property address, carrier, insured name, and estimate number, it emits a warning when documents disagree

This is intentionally conservative. The merger tries to keep the strongest visible value while still admitting that a conflict existed.

## Line-Item Deduplication Rules

Line items are merged across files because supplemental packets often repeat already-known items.

Current behavior:

- items are ordered deterministically before merge
- the dedupe key uses `dedupe_key`, unit price, replacement cost, actual cash value, and coverage name
- when duplicates are found, the stronger item wins
- missing fields are backfilled from the alternate item when safe
- notes from both copies are preserved
- a duplicate warning is added to the kept item notes

This is why contributors should avoid adding PDF-layout hacks in the export layer. Duplicate suppression belongs here.

## Totals Reconciliation Rules

Totals are not a simple sum of line items.

Current behavior:

- the merger chooses a primary totals source from the parsed document with the strongest totals coverage
- line-item math is still computed across the merged canonical line-item set
- missing totals may be backfilled from computed line-item values
- if summary replacement cost and computed line-item replacement cost diverge materially, the merger emits a warning instead of silently forcing agreement
- `net_payable`, `gross_acv`, `recoverable_depreciation`, and `total_if_incurred` are reconstructed when they can be inferred safely

This is one of the most important design decisions in the repo: stronger summary totals are often more trustworthy than noisy detail math on OCR-heavy packets.

## Roof Measurement Reconciliation

Roof measurements are merged field by field.

Current behavior:

- the largest extracted value wins when multiple documents disagree
- disagreement generates a warning
- `surface_area_sq_ft` and `squares` are backfilled from each other when one is missing

This rule is intentionally simple and should only be changed with real fixture evidence.

## Debug And Warning Surfaces

The merger writes its effects into two places:

- `CanonicalEstimate.warnings`
- `CanonicalEstimate.debug_notes`

Examples of merge-era issues that should remain visible:

- conflicting metadata across PDFs
- duplicate line items removed
- line-item totals disagreeing with summary totals
- conflicting roof measurements

## What Contributors Should Not Break

- deterministic ordering of merged documents and line items
- explicit warnings when important conflicts exist
- the rule that export consumes `CanonicalEstimate`, not raw parsed documents
- the ability to merge multi-PDF jobs without UI-specific logic

## When To Change This File

Touch `core/merge.py` when:

- supplemental documents are producing duplicate exported items
- metadata conflicts are resolved poorly
- totals fallback is too weak or too aggressive
- multi-file roof metrics are wrong

Do not change merge behavior just to fix one broken PDF until you confirm the issue is truly a cross-document reconciliation problem rather than a parser bug.

## Related Docs

- [CANONICAL_MODEL.md](./CANONICAL_MODEL.md)
- [DATA_FLOW_END_TO_END.md](./DATA_FLOW_END_TO_END.md)
- [../05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md](../05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md)
- [../06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md](../06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md)
