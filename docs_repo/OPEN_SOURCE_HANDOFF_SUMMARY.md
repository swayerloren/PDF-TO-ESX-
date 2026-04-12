# Open Source Handoff Summary

## What This Docs Repo Now Contains

`docs_repo/` now gives the project a durable knowledge structure for:

- onboarding
- product context
- architecture
- subsystem-level runtime behavior
- parser and export mapping
- testing and debugging
- contribution guidance
- project history
- release preparation
- developer reference

The repository root now complements that knowledge base with governance, support, release, and GitHub collaboration files needed for a public open-source release.

## How Future Developers Should Use It

| Goal | Where to start |
| --- | --- |
| understand the app quickly | `docs_repo/00_START_HERE/README_DOCS_REPO.md` |
| learn the runtime architecture | `docs_repo/02_ARCHITECTURE/` |
| change parser behavior | `docs_repo/02_ARCHITECTURE/PARSING_PIPELINE.md` and `docs_repo/06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md` |
| change merge behavior | `docs_repo/02_ARCHITECTURE/MERGE_AND_RECONCILIATION.md` |
| change ESX output | `docs_repo/02_ARCHITECTURE/ESX_GENERATION_FLOW.md` and `docs_repo/04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md` |
| debug failures | `docs_repo/05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md` |
| understand project evolution | `docs_repo/07_PROJECT_HISTORY/` |

Read architecture before changing parser or export logic. Update history docs when significant behavior changes land.

## Best Areas For Outside Contribution

- parser coverage for new carrier layouts
- OCR-heavy document recovery
- multi-PDF reconciliation improvements backed by fixture evidence
- fixture-based regression testing
- ESX compatibility research and validation
- documentation improvements tied to real code changes

## Highest-Value Next Improvements

1. expand parser regression coverage with real fixture sets
2. improve OCR-heavy metadata and line-item recovery
3. refine totals reconciliation for mixed packet types
4. strengthen ESX compatibility assumptions with better real-format evidence
5. package the desktop app more cleanly for non-developer users
