# How To Add New Parsers

## Scope

In this repo, "new parsers" usually means improving an existing extraction stage for a new carrier or layout pattern rather than creating a second end-to-end parser stack.

## Start With The Right Diagnosis

| Symptom | Likely file |
| --- | --- |
| guide/sample content leaking into output | `parsing/page_classifier.py` |
| missing claim/property metadata | `extract/metadata.py` |
| weak totals | `extract/totals.py` |
| broken detail rows | `extract/line_items.py` |
| weak roof metrics | `extract/measurements.py` |

## Recommended Process

1. identify which stage is actually failing
2. capture one or more real examples of the failing pattern
3. inspect `*.canonical.json` and warnings before touching XML output
4. add the smallest rule that fixes the pattern
5. run tests
6. re-check a layout that already worked
7. document the new behavior if coverage changed materially

## Parser Contribution Checklist

- did the change improve the canonical estimate?
- did the change avoid hardcoding fake values?
- did the change preserve existing working layouts?
- did the change produce clearer warnings when recovery is incomplete?

## Important Rule

If the parser learns something new, that knowledge should appear in the canonical estimate first. Do not patch XML output to compensate for parsing gaps.

## What To Watch Out For

- overfitting a rule to one sample
- reintroducing sample/guide-page pollution
- distorting line-item math for layouts that already worked
- converting warnings into silent wrong data

## Related Docs

- [../02_ARCHITECTURE/PARSING_PIPELINE.md](../02_ARCHITECTURE/PARSING_PIPELINE.md)
- [../04_MAPPING_AND_FORMATS/PDF_FIELD_MAPPING.md](../04_MAPPING_AND_FORMATS/PDF_FIELD_MAPPING.md)
- [../05_TESTING_AND_DEBUG/SAMPLE_PDF_BEHAVIOR.md](../05_TESTING_AND_DEBUG/SAMPLE_PDF_BEHAVIOR.md)
