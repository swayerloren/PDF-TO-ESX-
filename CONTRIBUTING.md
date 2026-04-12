# Contributing

`PDF TO ESX AGENT` is a real working desktop application, but it is still early-stage and heuristic in important areas. Good contributions improve real behavior without overstating compatibility or hiding uncertainty.

## Start Here

Read these first:

1. [README.md](README.md)
2. [docs_repo/00_START_HERE/QUICK_START_FOR_DEVELOPERS.md](docs_repo/00_START_HERE/QUICK_START_FOR_DEVELOPERS.md)
3. [docs_repo/06_CONTRIBUTING/CONTRIBUTING.md](docs_repo/06_CONTRIBUTING/CONTRIBUTING.md)
4. [docs_repo/02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md](docs_repo/02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)

## Best Entry Points

| If you want to... | Start here |
| --- | --- |
| improve parser quality | [docs_repo/06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md](docs_repo/06_CONTRIBUTING/HOW_TO_ADD_NEW_PARSERS.md) |
| improve ESX output | [docs_repo/06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md](docs_repo/06_CONTRIBUTING/HOW_TO_IMPROVE_ESX_OUTPUT.md) |
| understand the codebase layout | [docs_repo/06_CONTRIBUTING/CODEBASE_TOUR.md](docs_repo/06_CONTRIBUTING/CODEBASE_TOUR.md) |
| debug a regression | [docs_repo/05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md](docs_repo/05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md) |
| understand project tradeoffs | [docs_repo/03_ENGINEERING_DECISIONS/WHY_WE_BUILT_IT_THIS_WAY.md](docs_repo/03_ENGINEERING_DECISIONS/WHY_WE_BUILT_IT_THIS_WAY.md) |

## Branch Expectations

- use a short-lived topic branch for non-trivial work
- keep each pull request focused on one logical change
- avoid mixing parser, export, UI, and repo-process changes unless the change genuinely crosses those boundaries
- if you have direct maintainer access, still prefer pull requests for changes that affect behavior, compatibility, or release posture

## Pull Request Quality Bar

Every pull request should explain:

- what changed
- why it was needed
- which subsystem was affected
- what validation was performed
- what documentation changed

Use the repository pull request template.

## Testing Expectations

At minimum, run the checks relevant to your change:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall src run_app.py tests
```

When parser behavior changes:

- validate against at least one real or realistically redacted PDF layout if available
- inspect `*.canonical.json` before assuming the exporter is wrong
- update mapping or testing docs when the supported behavior changed materially

When ESX output changes:

- inspect both `*.esx.xml` and `*.canonical.json`
- keep `docs_repo/04_MAPPING_AND_FORMATS/` aligned with the code
- do not claim native proprietary compatibility without strong evidence

## Documentation Expectations

Update documentation when behavior or contribution guidance changes.

Common files to update:

- [CHANGELOG.md](CHANGELOG.md)
- [ROADMAP.md](ROADMAP.md)
- [docs_repo/04_MAPPING_AND_FORMATS/](docs_repo/04_MAPPING_AND_FORMATS/)
- [docs_repo/05_TESTING_AND_DEBUG/](docs_repo/05_TESTING_AND_DEBUG/)
- [docs_repo/06_CONTRIBUTING/](docs_repo/06_CONTRIBUTING/)
- [docs_repo/07_PROJECT_HISTORY/](docs_repo/07_PROJECT_HISTORY/)

## Sensitive Data Rule

Do not commit:

- unredacted insurance estimates
- customer or claimant personally identifying information
- secrets, tokens, or environment-specific credentials
- proprietary ESX artifacts you do not have the right to redistribute

If an issue needs a sample document, use a redacted sample or explain the layout in detail.

## Security

Normal parser bugs, unsupported layouts, and output mismatches should go through the normal issue templates.

Potential security vulnerabilities should follow [SECURITY.md](SECURITY.md), not public issues.

## Contributor Workflow

1. Read the relevant docs in `docs_repo/`.
2. Make the smallest correct change.
3. Run the relevant validation.
4. Update docs if behavior changed.
5. Open a pull request with evidence and risk notes.
