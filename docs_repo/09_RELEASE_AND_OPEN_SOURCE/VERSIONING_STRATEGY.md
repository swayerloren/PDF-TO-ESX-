# Versioning Strategy

## Current Starting Point

The repo currently documents itself as:

- `v0.1.0`

This is the first working open-source foundation release.

## Suggested Semantics

- patch version for bug fixes, documentation fixes, and non-breaking parser improvements
- minor version for meaningful parsing, canonical, export, or UI capability expansion
- major version for breaking canonical or export-contract changes

## Pre-1.0 Interpretation

Before `1.0.0`, this repo should still behave like a serious public project:

- avoid casual breaking changes just because the major version is zero
- document parser-behavior changes when they materially alter outputs
- treat canonical-model and export-structure changes as release-note-worthy even before `1.0.0`

## Practical Guidance

Examples:

- `0.1.1`
  parser bug fix, logging refinement, doc correction
- `0.2.0`
  significant new parser coverage, new canonical fields, new validation behavior
- `1.0.0`
  stable public contract with stronger compatibility guarantees

## What Must Trigger Extra Documentation

Update `CHANGELOG.md`, and usually `DECISION_LOG.md`, when a release changes:

- canonical field definitions
- merge or reconciliation rules
- XML structure or package contents
- setup requirements
- current claims about ESX compatibility

## Important Note

Because parser behavior affects output quality, even non-breaking parsing improvements should be documented carefully in the changelog.
