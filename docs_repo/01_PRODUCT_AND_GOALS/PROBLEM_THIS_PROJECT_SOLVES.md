# Problem This Project Solves

## The Core Problem

Insurance estimate PDFs are common, but they are difficult to use programmatically:

- different carriers format them differently
- some PDFs contain native text and some are mostly scanned images
- instructional pages and payment letters can be mixed into the same document
- totals and detail lines are often presented in inconsistent layouts

If the extracted data is not normalized, downstream export becomes fragile.

## Why This Is Hard

The same estimate packet can include:

- claim metadata
- estimate summary totals
- line-item pages
- roof geometry pages
- sample or guide pages that should not be parsed as real claim data

That means naive `PDF -> XML` conversion is brittle.

## What This Project Provides

This repo solves the problem with a staged pipeline:

1. detect whether pages are text-rich or scan-heavy
2. recover text as safely as possible
3. parse structured estimate data with deterministic heuristics
4. normalize the data into a canonical model
5. export from that model into ESX-style XML

## The Practical Benefit

Developers and operators get:

- a local desktop app instead of a mockup
- visible warnings and validation when parsing is incomplete
- inspectable artifacts instead of opaque conversions
- a codebase that can be tuned over time for new layouts
