# Public Positioning

## Recommended Public Description

Describe `PDF TO ESX AGENT` publicly as:

- a local Windows desktop app and open-source codebase for converting insurance estimate PDFs into structured ESX/XML outputs
- a domain-specific parser/export tool for real estimate packets, not a generic PDF utility
- a project that favors inspectability, deterministic output, and documented limitations over black-box claims

## How It Differs From Generic PDF Parsers

Generic PDF parsers usually stop at text extraction or table scraping.

This repo goes further by adding:

- insurance-estimate-aware page classification
- metadata, totals, line-item, and roof-measurement extraction
- canonical normalization before export
- deterministic ESX/XML generation
- package validation and user-facing validation messages

That is the core positioning difference: it is not just “read text from a PDF.” It is a structured estimate-to-export workflow.

## How It Differs From Closed Insurance-Industry Tools

This repo is different from closed tools because it is:

- local-first rather than cloud-dependent
- inspectable at every stage
- explicit about assumptions and limitations
- documented for outside contributors
- designed so parser logic, canonical mapping, and export logic can be improved independently

It should be positioned as a transparent tool and engineering foundation, not as a turnkey enterprise claims platform.

## Claims That Should Not Be Made Yet

Do not claim that the repo:

- supports every carrier or estimate layout
- writes a proprietary native `XACTDOC.ZIPXML` file
- is a drop-in replacement for commercial estimating platforms
- is fully validated across broad real-world production datasets
- is an installer-grade desktop product for non-technical end users
- is affiliated with carriers, Xactimate, or other proprietary vendors

## What Early Adopters Should Expect

Early adopters should expect:

- a real working app
- meaningful value on supported and moderately messy estimate PDFs
- strong documentation and inspectable output
- warnings when confidence is lower or totals need reconciliation
- a project that still benefits from layout-specific tuning and broader regression coverage

## Best-Fit Contributors Right Now

The best contributors for the current stage are:

- developers who can improve parser coverage for real estimate layouts
- contributors who can help with OCR-heavy recovery
- people who can strengthen ESX/XML validation and compatibility evidence
- Windows packaging and release contributors
- maintainers who can improve fixture strategy, documentation, and issue triage

## Recommended Tone For Public Messaging

Use a tone that is:

- specific
- honest
- technically credible
- helpful to both developers and industry operators

Avoid language that feels:

- hype-driven
- “AI magic” oriented
- vague about output quality
- dismissive of the hard parts of insurance estimate parsing

## Related Docs

- [GITHUB_DISCOVERABILITY.md](./GITHUB_DISCOVERABILITY.md)
- [REPO_DESCRIPTION_OPTIONS.md](./REPO_DESCRIPTION_OPTIONS.md)
- [GITHUB_SOCIAL_PREVIEW_PLAN.md](./GITHUB_SOCIAL_PREVIEW_PLAN.md)
