# GitHub Release Checklist

## Code And Docs

- confirm `README.md` matches the current repo state
- confirm `docs_repo/` links are correct
- confirm `CHANGELOG.md` is updated
- confirm `ROADMAP.md` still reflects the real priority tracks
- confirm `KNOWN_LIMITATIONS` and ESX assumptions are honest
- confirm root governance and support files are present and aligned

## Validation

- run unit tests
- run compileall
- run `.\scripts\Verify-Clean-Environment.ps1`
- run `.\scripts\Build-Windows-Exe.ps1`
- launch `dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`
- run at least one real conversion smoke with a local fixture
- run at least one packaged conversion smoke with a local fixture when shipping a desktop artifact

## Repo Hygiene

- confirm runtime artifacts are not committed accidentally
- confirm `sample_output/generated/` is clean
- confirm logs are not checked in
- confirm dependency file is current
- confirm `requirements-build.txt` and `PDF-TO-ESX-Agent.spec` are current
- confirm docs point to files that actually exist
- confirm issue templates, PR template, and workflows are present

## Release Metadata

- tag the version
- publish release notes from `CHANGELOG.md`
- include known limitations and current compatibility language
- avoid overstating ESX compatibility or parser coverage
- confirm the public release notes draft still matches the actual repo state
- confirm packaged-build docs still match the real artifact layout

## After Release

- capture follow-up gaps in `ROADMAP.md`
- add any architectural decisions triggered by feedback to `DECISION_LOG.md`
- update `PUBLIC_REPO_COMPLETION_STATUS.md` if the public-release posture changed materially
