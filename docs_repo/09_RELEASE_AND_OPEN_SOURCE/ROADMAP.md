# Roadmap

## How To Read This Roadmap

This roadmap is intentionally conservative. It reflects what would most improve the current codebase, not a generic wishlist.

## Current Priority Tracks

| Track | Current state | Why it matters | Good contribution entry point |
| --- | --- | --- | --- |
| fixture-based parser regression coverage | weak | parser improvements are still easier to break than to prove | `tests/`, `docs_repo/05_TESTING_AND_DEBUG/` |
| OCR-heavy recovery | partial | scanned documents remain the weakest real-world case | `parsing/document_loader.py`, `ocr/rapid_ocr.py`, `extract/line_items.py` |
| totals reconciliation | partial | mixed packets and noisy tables still create warning-heavy outputs | `extract/totals.py`, `core/merge.py` |
| ESX compatibility research | partial | current package is useful but not yet a native proprietary writer | `export/esx_writer.py`, `export/validator.py` |
| contributor friendliness | improving | the repo now has strong docs, root governance files, and GitHub templates, but tests and sharable fixtures can improve onboarding further | `docs_repo/`, root repo files, `tests/` |

## Near-Term Work

1. add broader fixture-driven regression tests for metadata, totals, and line-item parsing
2. improve OCR-heavy metadata and line-item recovery
3. reduce false-positive warnings where canonical output is already strong
4. keep sharpening docs and contribution paths as new contributors arrive

## Medium-Term Work

- richer parser diagnostics in canonical output
- more explicit carrier/layout tagging in warnings
- better sharable sample strategy for open-source testing
- stronger validation around assumptions in the current XML package
- installer/signing evaluation for public Windows distribution

## Long-Term Work

- native proprietary ESX packing if sufficiently documented
- broader export support beyond the current XML/ESX-style package
- stronger automated parser benchmark datasets

## Not A Current Priority

- cloud parsing services
- turning the repo into a full claims platform
- building a large multi-user web application around the current codebase
