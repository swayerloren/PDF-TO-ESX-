# Edge Case Examples

## Scan-Heavy Packet

Expected behavior:

- OCR may run on many pages
- metadata may still be partially incomplete
- totals may rely more heavily on summary text than detail-line math

## Letter + Estimate Bundle

Expected behavior:

- payment-letter or explanation content may exist alongside estimate pages
- guide/sample pages should be excluded when known patterns match
- some estimate-number fields may still remain blank

## Duplicate Detail Sections

Expected behavior:

- canonical merge may remove duplicate line items
- warnings should explain that duplicates were removed

## Weak Native Text But OCR Available

Expected behavior:

- native text is attempted first
- OCR replaces native text only when the OCR result appears materially stronger

## Broken Or Empty PDF

Expected behavior:

- conversion stops with a clear error
- no export is written
