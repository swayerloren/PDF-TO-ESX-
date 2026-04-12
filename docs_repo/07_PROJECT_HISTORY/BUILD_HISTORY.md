# Build History

## Foundation Build

The project started as a standalone desktop app focused on one workflow:

`insurance estimate PDF -> canonical estimate -> ESX-style export`

The first build established:

- Tk desktop UI
- local PDF ingestion
- OCR-aware fallback
- staged extractors
- canonical model
- XML/package writer

## Hardening Pass

The next major pass focused on reliability:

- improved page classification for sample/guide pages
- better metadata extraction on mixed packets
- improved line-item financial parsing
- clearer failure handling for unreadable PDFs and empty parses
- XML and package validation after write
- stronger UI success and warning states

## Final Engineering Pass

The engineering cleanup pass focused on maintainability:

- removed dead code
- tightened output/path handling
- made output stems deterministic for merged selections
- improved logger hierarchy and stage prefixes
- added clean-environment verification
- cleaned runtime artifacts out of the final repo state

## Open-Source Handoff Pass

The current pass adds the durable documentation structure in `docs_repo/` so external developers can understand the project, run it, extend it, and track how it changes over time.
