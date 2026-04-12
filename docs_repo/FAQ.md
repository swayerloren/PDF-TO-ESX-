# FAQ

## Is this a real working app?

Yes. It is a runnable Windows desktop app with a real PDF-processing pipeline and real output artifacts.

## Does it use cloud OCR or cloud AI APIs?

No. The current implementation is local-first and does not depend on cloud parsing services.

## Does it support scanned PDFs?

Yes, to a degree. It detects text-poor pages and can apply local OCR when dependencies are available. Scanned PDFs remain harder than native-text PDFs.

## Does it write a native Xactimate ESX file?

Not in the proprietary `XACTDOC.ZIPXML` sense. It writes a standards-based `.esx` zip package containing `XACTDOC.XML`, `canonical_estimate.json`, and `manifest.json`.

## Why is there a `*.canonical.json` output?

Because the project uses a canonical estimate boundary between parsing and export. That file is the easiest way to inspect what the parser actually produced before looking at XML.

## Why not convert directly from PDF to XML?

Because estimate PDFs are noisy and inconsistent. The canonical model isolates parser uncertainty from export logic and makes the codebase much easier to debug and evolve.

## Where do I start if parsing is wrong?

Start with:

- [./05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md](./05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md)
- `logs/pdf_to_esx_agent.log`
- the generated `*.canonical.json`

## Where do I add support for a new carrier layout?

Usually in:

- `src/pdf_to_esx_agent/extract/metadata.py`
- `src/pdf_to_esx_agent/extract/line_items.py`
- `src/pdf_to_esx_agent/extract/totals.py`
- `src/pdf_to_esx_agent/parsing/page_classifier.py`

See:

- [./06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md](./06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md)

## Where do I look if multi-PDF jobs behave strangely?

Start with:

- [./02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md](./02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md)
- [./02_ARCHITECTURE/CANONICAL_MODEL.md](./02_ARCHITECTURE/CANONICAL_MODEL.md)
- [./05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md](./05_TESTING_AND_DEBUG/COMMON_FAILURE_PATTERNS.md)

## Why was SALES FORCE AGENT referenced?

The source repo contained useful patterns for OCR-aware ingestion, staged parsing, canonical normalization, and ESX structure references. This project reused those ideas but deliberately did not import unrelated Salesforce runtime and platform systems.

## Is the project cross-platform?

The current target is Windows + local Python + VS Code. The code is mostly Python, but the app and scripts are documented and validated primarily for Windows.

## What are the best first contributions?

- parser coverage for new layouts
- OCR-heavy recovery improvements
- fixture-based regression tests
- better ESX compatibility evidence and validation

## Where should I start if I only want the shortest path into the repo?

Read in this order:

1. [./00_START_HERE/PROJECT_OVERVIEW.md](./00_START_HERE/PROJECT_OVERVIEW.md)
2. [./00_START_HERE/QUICK_START_FOR_DEVELOPERS.md](./00_START_HERE/QUICK_START_FOR_DEVELOPERS.md)
3. [./02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](./02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
4. [./06_CONTRIBUTING/CODEBASE_TOUR.md](./06_CONTRIBUTING/CODEBASE_TOUR.md)

## Why are sample PDFs not in this repo?

Real estimate PDFs may have sharing, privacy, or licensing constraints. The project documents the fixture behavior and paths used during development without assuming those inputs can be redistributed publicly.
