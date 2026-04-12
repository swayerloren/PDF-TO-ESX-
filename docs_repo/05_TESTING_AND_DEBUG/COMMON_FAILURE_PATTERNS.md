# Common Failure Patterns

## Broken Or Unreadable PDFs

Symptoms:

- zero readable pages
- immediate conversion failure

Likely cause:

- invalid file content or non-standard PDF damage

Handled by:

- `ConversionError` before export

## Scan-Heavy PDFs With Weak OCR

Symptoms:

- no usable line items
- incomplete insured/address extraction
- large summary-vs-detail mismatch warning

Likely cause:

- weak scan quality or broken table recognition

## Mixed Packet Noise

Symptoms:

- guide or sample text leaking into parsed metadata
- odd titles or totals from non-estimate pages

Likely cause:

- page classification missed a non-claim page pattern

## Line Item Column Misread

Symptoms:

- strange unit price
- ACV and depreciation swapped or distorted
- unrealistic total math

Likely cause:

- an unfamiliar carrier row layout or percentage token pattern

## Output Validation Failure

Symptoms:

- conversion reaches export stage but fails before success

Likely cause:

- XML structure issue
- package contents mismatch
- bad summary-reference linkage

This is rare in current code because the writer validates before reporting success.
