# Contributing

## Goal

Contributions should improve the project without blurring the core boundaries:

- ingestion and OCR
- parsing
- canonical normalization
- export and validation
- UI orchestration

## Best Contribution Types

| Type | Why it helps |
| --- | --- |
| better parser coverage for real estimate layouts | highest leverage for data quality |
| stronger fixture-based tests | lowers regression risk |
| improved XML/ESX compatibility work | improves downstream usefulness |
| clearer validation and debugging behavior | helps both operators and contributors |
| docs tied to actual code behavior | keeps the project maintainable |

## Read Before You Change Code

1. [../00_START_HERE/QUICK_START_FOR_DEVELOPERS.md](../00_START_HERE/QUICK_START_FOR_DEVELOPERS.md)
2. [../02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](../02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
3. [../02_ARCHITECTURE/CANONICAL_MODEL.md](../02_ARCHITECTURE/CANONICAL_MODEL.md)
4. [../03_ENGINEERING_DECISIONS/WHY_WE_BUILT_IT_THIS_WAY.md](../03_ENGINEERING_DECISIONS/WHY_WE_BUILT_IT_THIS_WAY.md)

## Contribution Paths

| If you want to... | Start here |
| --- | --- |
| improve scan handling | [../02_ARCHITECTURE/OCR_AND_SCAN_STRATEGY.md](../02_ARCHITECTURE/OCR_AND_SCAN_STRATEGY.md) |
| improve parsing | [HOW_TO_ADD_NEW_PARSERS.md](./HOW_TO_ADD_NEW_PARSERS.md) |
| improve export output | [HOW_TO_IMPROVE_ESX_OUTPUT.md](./HOW_TO_IMPROVE_ESX_OUTPUT.md) |
| improve setup or onboarding | [DEVELOPMENT_SETUP.md](./DEVELOPMENT_SETUP.md), [../FAQ.md](../FAQ.md) |
| improve docs or release process | [../09_RELEASE_AND_OPEN_SOURCE/OPEN_SOURCE_READINESS.md](../09_RELEASE_AND_OPEN_SOURCE/OPEN_SOURCE_READINESS.md) |

## Contributor Rules

- keep changes scoped
- prefer improving one stage of the pipeline at a time
- do not bypass the canonical model
- do not hide parser uncertainty by silently inventing output data
- update docs when behavior meaningfully changes
- if you change a contract, update the relevant mapping/reference docs too

## Validation Expectation

- run the relevant automated checks
- when parser behavior changes, validate against at least one real PDF layout if available
- when export behavior changes, inspect both `*.canonical.json` and `*.esx.xml`

## Docs To Update When Behavior Changes

| Change area | Docs that should usually move with it |
| --- | --- |
| parser behavior | `docs_repo/04_MAPPING_AND_FORMATS/`, `docs_repo/05_TESTING_AND_DEBUG/`, `CHANGELOG.md` |
| canonical contract | `CANONICAL_MODEL.md`, `ESTIMATE_DATA_MODEL_REFERENCE.md`, `CHANGELOG.md` |
| export structure | `ESX_GENERATION_FLOW.md`, `CANONICAL_TO_ESX_MAPPING.md`, `XML_ESX_ASSUMPTIONS.md`, `CHANGELOG.md` |
| release posture | `OPEN_SOURCE_READINESS.md`, `ROADMAP.md`, `CHANGELOG.md` |
