# Decision Log

Use this log for decisions that shape architecture, compatibility claims, or contributor expectations.

## Decision Index

| Date | Decision |
| --- | --- |
| 2026-04-12 | keep a canonical estimate boundary between parsing and export |
| 2026-04-12 | use selective OCR instead of OCR on every page |
| 2026-04-12 | ship a standards-based `.esx` package now instead of waiting for a native proprietary writer |
| 2026-04-12 | keep the UI thin and route conversion through `ConversionService` |
| 2026-04-12 | treat known guide/sample pages as non-claim content |
| 2026-04-12 | prefer stronger summary totals over noisy detail math when they conflict materially |
| 2026-04-12 | keep the project local-first and avoid cloud parsing dependencies |

## Entry 1

### Date

2026-04-12

### Decision

Use a canonical estimate model between PDF parsing and ESX generation.

### Context

Estimate PDFs are inconsistent and the export format has compatibility assumptions that may change over time.

### Why

This keeps parser heuristics, merge logic, and export rules from being tightly coupled.

### Consequences

- easier debugging
- clearer module boundaries
- exporter can evolve without understanding PDF internals

### Follow-up needed

- expand canonical fields only when multiple pipeline stages benefit

## Entry 2

### Date

2026-04-12

### Decision

Use selective OCR instead of OCR on every page.

### Context

Many estimate PDFs already contain usable native text, while full-document OCR is slower and can degrade good pages.

### Why

Selective OCR preserves better native text where available and keeps scan-heavy recovery focused on weak pages.

### Consequences

- better performance on native-text PDFs
- more complex ingestion logic
- OCR quality remains a major factor on degraded scans

### Follow-up needed

- keep improving page routing heuristics with real fixtures

## Entry 3

### Date

2026-04-12

### Decision

Ship a standards-based `.esx` zip package with `XACTDOC.XML` instead of delaying the project for a native proprietary writer.

### Context

Real ESX references showed useful XML structure, but the repo did not have a native `XACTDOC.ZIPXML` writer implementation.

### Why

A deterministic inspectable package is more useful today than a theoretical native writer that is not implemented.

### Consequences

- working export exists now
- ESX compatibility is incomplete by native proprietary standards
- the writer remains replaceable later

### Follow-up needed

- gather stronger evidence before implementing a native packer

## Entry 4

### Date

2026-04-12

### Decision

Keep the UI thin and push all conversion logic through `ConversionService`.

### Context

UI-driven business logic would make parsing and export harder to test and reuse.

### Why

The conversion pipeline needs one clear orchestration path for validation, logging, and errors.

### Consequences

- UI is easier to maintain
- conversion behavior is easier to test
- background threading stays isolated to the view layer

### Follow-up needed

- keep future features from bypassing `ConversionService`

## Entry 5

### Date

2026-04-12

### Decision

Treat known guide and sample pages as non-claim content.

### Context

Real carrier packets often include instructional pages that can corrupt metadata and line-item parsing if treated as estimate data.

### Why

Excluding known non-claim content improves parser precision more than trying to recover from polluted output later.

### Consequences

- page classification becomes a critical parser-quality dependency
- new carrier guide formats may still need classifier updates

### Follow-up needed

- extend non-claim page patterns with real fixtures rather than speculation

## Entry 6

### Date

2026-04-12

### Decision

Prefer stronger summary totals over noisy detail math when they conflict materially.

### Context

Detail-line parsing is more fragile than summary parsing, especially on OCR-heavy or mixed-layout documents.

### Why

This keeps canonical totals usable while still surfacing reconciliation warnings for review.

### Consequences

- totals may remain trustworthy even when some line items are noisy
- contributors must not assume line-item sums are always the primary truth source

### Follow-up needed

- improve line-item parsing while keeping reconciliation warnings honest

## Entry 7

### Date

2026-04-12

### Decision

Keep the project local-first and avoid cloud parsing dependencies.

### Context

The project goal is a runnable, inspectable desktop tool with minimal operational dependency.

### Why

Local-first behavior improves privacy, reproducibility, contributor access, and architectural clarity.

### Consequences

- OCR quality and throughput are bounded by local dependencies
- there is no cloud fallback for weak scans

### Follow-up needed

- keep evaluating local-only improvements before introducing any hosted dependency
