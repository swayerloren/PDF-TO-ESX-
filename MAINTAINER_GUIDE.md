# Maintainer Guide

This guide is for the people reviewing issues, pull requests, releases, and public claims about the project.

## Triage The Issue First

Classify incoming issues before responding in detail.

| Issue type | Where it usually belongs |
| --- | --- |
| setup problem | docs or environment issue |
| missing field or unsupported layout | parser or page-classification issue |
| duplicate items or conflicting totals across PDFs | merge/reconciliation issue |
| XML mismatch or import problem | export or compatibility issue |
| vulnerability | security process, not public triage |

## Parser Bug Versus ESX Bug

Use the generated artifacts to decide where the failure actually lives.

If `*.canonical.json` is wrong:

- the bug is usually in ingestion, parsing, or merge logic

If `*.canonical.json` looks right but `*.esx.xml` is wrong:

- the bug is usually in `export/esx_writer.py` or export mapping assumptions

If both artifacts look correct but a downstream tool still rejects the file:

- the issue is likely an ESX compatibility problem, a packaging assumption problem, or a downstream import expectation that needs better evidence

## Prioritization Guidance

Prefer issues that improve correctness and trust:

1. reproducible parser bugs on real estimate layouts
2. output bugs that generate invalid or misleading XML/package content
3. regressions in deterministic naming, validation, or clear error handling
4. contributor and debugging documentation gaps that block quality contributions
5. cosmetic improvements that do not change behavior

## Review Outside PRs Safely

Check all of the following:

- the change touches the right subsystem
- the contributor did not bypass the canonical model
- the PR does not silently invent data to hide parser gaps
- tests were run and described
- docs were updated when behavior changed
- no private or unredacted estimate files were committed
- compatibility claims are matched to actual evidence

## Standards To Enforce

- parser logic belongs in parsing and extract stages
- merge logic belongs in `core/merge.py`
- export logic belongs in the exporter and validator
- the UI should stay thin
- warnings should remain visible when certainty is incomplete
- public docs should describe the current system honestly

## When To Update `docs_repo`

Update `docs_repo` when a change affects:

- architecture or subsystem boundaries
- parser or mapping behavior
- canonical model fields
- merge or reconciliation rules
- export structure or assumptions
- contributor workflow or release posture

At minimum, keep these aligned:

- root `README.md`
- root `CHANGELOG.md`
- root `ROADMAP.md`
- `docs_repo/04_MAPPING_AND_FORMATS/`
- `docs_repo/07_PROJECT_HISTORY/`
- `docs_repo/09_RELEASE_AND_OPEN_SOURCE/`

## Handling Breaking Mapping Or Schema Changes

If a change alters canonical fields, XML structure, package contents, or compatibility claims:

1. require a clear rationale
2. require updated mapping docs
3. require updated changelog and decision log entries
4. require explicit backward-compatibility notes in the PR
5. avoid merging until the public docs match the new behavior

## Security And Conduct

- route vulnerabilities to [SECURITY.md](SECURITY.md)
- route conduct concerns through [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- do not ask reporters to post sensitive details publicly

## Release Discipline

Before tagging a release:

- use [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)
- confirm workflows still reflect the real stack
- confirm issue templates and governance files are present
- confirm the project does not claim more compatibility than it currently has
