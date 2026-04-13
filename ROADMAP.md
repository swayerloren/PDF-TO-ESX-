# Roadmap

This roadmap reflects the real current project, not an aspirational product rewrite.

Detailed release posture and open-source context live in [docs_repo/09_RELEASE_AND_OPEN_SOURCE/](docs_repo/09_RELEASE_AND_OPEN_SOURCE/).

## Current Priority Tracks

| Track | Status | Why it matters |
| --- | --- | --- |
| fixture-based parser regression coverage | needed | parser improvements are still easier to break than to prove |
| OCR-heavy recovery | partial | scanned estimate packets remain the hardest real-world case |
| totals reconciliation | partial | summary/detail conflicts still produce important warnings |
| ESX compatibility evidence | partial | current output is deterministic and validated, but not a native proprietary writer |
| contributor readiness | improving | public docs are strong now, but sharable fixtures and broader tests would improve outside contribution velocity |

## Near-Term Priorities

1. expand fixture-driven regression tests for metadata, totals, and line items
2. improve OCR-heavy extraction reliability
3. reduce false-positive warnings while keeping uncertainty honest
4. gather better evidence for ESX compatibility improvements
5. harden the packaged Windows release story with repeatable validation and clearer distribution guidance
6. continue tightening contribution and release processes as outside contributors arrive

## Explicit Non-Goals Right Now

- cloud parsing services
- turning the project into a claims platform
- claiming universal carrier or estimate-layout coverage
- claiming native proprietary ESX compatibility without evidence
