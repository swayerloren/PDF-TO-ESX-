# Open Source Readiness

## Readiness Snapshot

| Area | State | Notes |
| --- | --- | --- |
| runnable app | ready | desktop app launches and converts PDFs locally |
| architecture docs | ready | `docs_repo/` now covers the major subsystems |
| contributor onboarding | ready with follow-up room | root and `docs_repo` contribution paths now exist, but sharable fixture coverage can still improve |
| governance and community files | ready | license, conduct, support, security, PR template, and issue templates are now present |
| parser coverage claims | partial | meaningful real coverage exists, but not universal layout support |
| export compatibility claims | partial | deterministic and validated, but not a native proprietary writer |
| packaging for non-developers | not ready | no installer or standalone distribution yet |

## What Is Ready

- the app is runnable locally
- the parser/export boundary is clear
- tests and clean-environment verification exist
- current ESX assumptions and limitations are documented
- contributor guidance now exists in `docs_repo/`
- public root repo assets now exist for GitHub release readiness

## What Is Not Fully Ready Yet

- no packaged installer or standalone executable
- no broad fixture-based regression suite committed to the repo
- no native proprietary ESX packer
- parser coverage is not yet broad enough to claim universal estimate support
- hosted-repo settings such as private vulnerability reporting still need maintainer configuration

## Why The Repo Is Still Worth Publishing

The codebase already has real value as:

- a working local app
- a readable architecture reference
- a contributor-friendly starting point for estimate parsing and ESX export work

## Before A Public Release

- review docs for link accuracy
- confirm setup steps on a clean machine
- decide what sample fixtures can be shared publicly
- enable GitHub Private Vulnerability Reporting
- make sure release notes state the current ESX and parser limits plainly
