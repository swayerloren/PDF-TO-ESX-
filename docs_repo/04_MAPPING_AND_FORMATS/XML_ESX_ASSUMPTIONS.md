# XML ESX Assumptions

## Current Reality

The app writes a standards-based `.esx` zip package containing `XACTDOC.XML`.

It does not currently write the proprietary `XACTDOC.ZIPXML` packing used by some native Xactimate ESX files.

## Assumptions The Current Writer Makes

### XML Root

- the export root should be `XACTDOC`

### Useful Sections

- `PROJECT_INFO`
- `CLAIM_INFO`
- `GROUP`
- `EMBEDDED_PL`
- `TOTALS`
- `SOURCE_DOCUMENTS`
- `VALIDATION`

These sections were chosen because they align with real ESX fixture structure observed in the source-agent repo and because they are sufficient for the current canonical model.

### Grouped Item + Summary Pattern

The writer assumes the dual representation below is useful and structurally consistent:

- `GROUP/ITEMS/ITEM`
- `EMBEDDED_PL/SUMITEMS/SUMITEM`

This is why the validator enforces `SUMMARY_REF` integrity.

### Package Assumption

The app assumes a practical package can be represented as:

- one XML payload
- one canonical JSON payload
- one manifest file

This is an engineering decision for inspectability and determinism, not proof that native Xactimate uses the same outer packaging.

## What Is Supported By Evidence

- real ESX fixtures contain `XACTDOC` XML structures
- sections such as `PROJECT_INFO`, `GROUP`, `PARAMS`, `ADM`, `CLAIM_INFO`, `CONTACTS`, and `EMBEDDED_PL` are present in those fixtures

## What Is Still An Assumption

- that the current open package layout is sufficient for every downstream ESX consumer
- that the chosen subset of fields is enough for desired import behavior
- that all important Xactimate semantics are represented yet

Future contributors should treat this document as a boundary between verified structure and open assumptions.
