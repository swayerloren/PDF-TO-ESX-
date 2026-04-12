# Sample PDF Behavior

## Current Known Fixture Behavior

The project has been tested against multiple estimate PDFs from:

- `C:\Users\LJ\AGENTS\SALES FORCE AGENT\TEST FILES\SCOPES`

## Representative Behaviors

| Sample type | Current behavior |
| --- | --- |
| clean native-text scope | generally strong parse |
| mixed letter + estimate bundle | usually converts, may rely on fallback totals or warnings |
| guide/sample pages included | current classifier excludes common known examples |
| scanned/OCR-heavy estimate | can convert, but warnings are more likely |
| repeated sections/pages | may deduplicate line items with warnings |

## Known Strong Cases

- State Farm sample/guide pages now stay out of the main parse path
- Allstate guide/sample pages no longer pollute metadata and line items
- multiple native estimate layouts convert successfully end to end

## Known Weak Case Family

- OCR-heavy Farmers-style scans remain the weakest area for metadata completeness and line-item/summary reconciliation

## Why This Matters

Outside contributors should not assume all PDFs behave the same. New parser work should be tested against more than one layout whenever possible.
