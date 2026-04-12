# Error Handling Reference

## Main Error Type

- `ConversionError`

This is the primary user-facing failure type for bad inputs, unusable PDFs, invalid output paths, and structurally unusable conversion results.

## Export Validation Error

- `ExportValidationError`

This error type is raised in the export validator and wrapped by `ConversionService` as a `ConversionError` before surfacing to the UI.

## Error-Handling Strategy

- fail early on bad file paths and non-PDFs
- fail before export when parsing yields no usable estimate data
- fail after export attempt if XML/package validation does not pass
- show clear error messages in the UI instead of raw tracebacks

## Common Failure Gates In `ConversionService`

| Gate | Example message intent |
| --- | --- |
| selected file does not exist | stop before parsing starts |
| selected file is not a PDF | reject invalid input immediately |
| output path is not a folder | prevent writing into an invalid destination |
| no readable text was extracted | explain whether scan/OCR conditions were involved |
| no line items and no usable totals | reject empty or structurally useless parses |
| export package validation failed | prevent false-success output reporting |

## Warning Strategy

Not every problem is fatal.

Warnings are used when:

- metadata is incomplete
- totals are reconstructed
- duplicate line items are removed
- scan-heavy pages did not benefit from OCR enough
- summary totals and detail totals disagree materially

Warnings should stay visible in:

- the UI status panels
- the canonical JSON artifact
- the runtime log

## Related Docs

- [./LOGGING_REFERENCE.md](./LOGGING_REFERENCE.md)
- [../05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md](../05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md)
- [../05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md](../05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md)
