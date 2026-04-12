# Major Milestones

## Milestone 1: End-To-End Conversion Exists

The project moved from idea to working software:

- PDFs can be selected in the UI
- parsing runs locally
- ESX-style output is generated on disk

## Milestone 2: Canonical Boundary Locked In

The app established `CanonicalEstimate` as the stable boundary between parsing and export. This is the architectural milestone that makes future improvements manageable.

## Milestone 3: Reliability Hardening

The app gained:

- stronger page classification
- better parser fallback behavior
- explicit user-facing failures
- package validation

This moved the repo from “working prototype” toward “maintainable tool.”

## Milestone 4: Clean Engineering Base

The final engineering pass left the repo in a cleaner state:

- dead code removed
- logging tightened
- deterministic output naming
- clean-environment startup verified

## Milestone 5: Open-Source Documentation Foundation

`docs_repo/` now provides a durable handoff structure for outside developers and future maintainers.
