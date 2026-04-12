# Why We Built It This Way

## The Short Version

We built the app as a staged local pipeline because estimate PDFs are messy and ESX output should still be deterministic.

## Why Canonical Normalization Exists

PDF parsing is uncertain by nature:

- OCR may help some pages and hurt others
- metadata can conflict across multiple files
- totals and line-item math can disagree
- some fields are present only in certain layouts

The canonical layer turns that uncertainty into one normalized estimate with warnings, provenance, and predictable structure.

## Why ESX Generation Is Separate

Export should consume structured data, not parser internals.

That separation is important because:

- ESX assumptions are still evolving
- the current package is standards-based, not proprietary-native
- future work may replace the writer or package format

If parsing and export were fused, every export change would risk parser regressions.

## Why We Reused Only Part Of SALES FORCE AGENT

The source repo had useful patterns for OCR-aware PDF ingestion, page classification, staged estimate parsing, canonical modeling, and ESX structure references. It also had many systems this project did not need, including Salesforce orchestration, runtime supervision, and broader claim-packet workflows.

This repo reused the useful ideas, not the unrelated platform complexity.
