# Example Inputs

## Supported Input Shape

The app expects one or more `.pdf` files that contain insurance estimate content.

## Real Input Categories Already Observed

| Input category | Example behavior |
| --- | --- |
| clean native estimate PDF | strong parse, minimal warnings |
| carrier letter + estimate bundle | often converts, may need fallback totals or metadata recovery |
| estimate with sample/guide pages | current classifier removes common known guide pages |
| scanned multi-page estimate | OCR can recover text, but warnings are more likely |
| repeated-page or repeated-section packet | canonical merge may deduplicate overlapping lines |

## Representative Fixture Names Used During Validation

- `Statefarm estimate.pdf`
- `Tripathi Allstate original scope.pdf`
- `Tripathi updated scope.pdf`
- `Vaji Bhimani insurance scope (1).pdf`
- `Adobe Scan Sep 9, 2025.pdf`

## Input Rules

- file must exist
- file must have `.pdf` extension
- PDFs can be selected individually or in a group
- duplicate selections are ignored during conversion normalization
