# Open Source Philosophy

## Why This Project Is Open Source

`PDF TO ESX AGENT` solves a practical conversion problem that many teams hit in slightly different ways: insurance estimate PDFs are messy, inconsistent, and often hard to turn into structured data safely.

Open-sourcing the project makes the work inspectable and improvable:

- the parsing logic can be reviewed instead of treated like a black box
- the export assumptions can be challenged and improved with evidence
- new layouts and edge cases can be contributed by the people who actually encounter them
- the documentation can grow with the software instead of lagging behind it

## Why The License Is Apache 2.0

The project uses the Apache License 2.0 because it is permissive, widely understood, and practical for both individual and commercial use.

It also includes an explicit patent grant, which is helpful for a project centered on parsing, transformation, and export logic that other teams may want to adapt or integrate.

The goal is to make reuse straightforward while keeping contribution and attribution expectations clear.

## What Contributions Matter Most

The highest-value contributions are the ones that improve real behavior:

- better parser support for real estimate layouts
- better OCR-heavy recovery
- stronger multi-file merge behavior
- stronger regression tests
- better ESX compatibility evidence and validation
- clearer debugging and contributor documentation

## Why Real-World PDFs Matter

This project is not a synthetic parsing exercise.

The hard problems come from real packets:

- carrier guide pages mixed into estimates
- degraded scans
- totals that disagree with detail math
- supplements that repeat earlier items
- line-item tables that are only partially machine-readable

That is why fixture evidence, redacted examples, and careful output inspection matter so much.

## Why Canonical Normalization Matters

The project deliberately separates:

- PDF ingestion
- structured extraction
- canonical normalization
- ESX generation

That boundary is not academic. It is what keeps parser uncertainty from leaking directly into export code and what makes the project maintainable for outside contributors.

## Why Reproducibility Matters

Claims about parser quality or ESX compatibility should be backed by:

- a reproducible input case
- a visible canonical output
- a visible XML output
- clear logs or warnings

Without that discipline, the project becomes harder to trust and harder to improve.

## Why Honesty About Limitations Matters

This repo is useful today, but it is not finished.

It is better to state clearly that:

- parser coverage is heuristic
- scanned PDFs are harder
- `.esx` output is standards-based rather than a proven native proprietary writer

than to publish vague or inflated compatibility claims.

Trust matters more than marketing language in a project like this.
