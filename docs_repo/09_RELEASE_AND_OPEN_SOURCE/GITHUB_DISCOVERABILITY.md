# GitHub Discoverability

## Purpose

This file recommends GitHub Topics for `PDF TO ESX AGENT` so the repository is easier to find and easier to classify correctly when developers and insurance-industry users land on it.

The goal is accuracy first. Topics should improve search relevance without overstating coverage, maturity, or proprietary compatibility.

## Topic Selection Principles

- prefer topics that describe what the repo actually does today
- prioritize search terms that match developer intent and insurance-workflow intent
- avoid broad marketing labels that could imply unsupported platform scope
- keep the final set compact enough to stay intentional

## Core Function Topics

| Topic | Why it helps | Recommend |
| --- | --- | --- |
| `pdf` | broadest entry point for document-processing search | yes |
| `pdf-parser` | tells developers this is not just a viewer or converter shell | yes |
| `data-extraction` | captures the structured-extraction use case beyond PDFs alone | yes |
| `document-processing` | fits the pipeline and helps with broader workflow discovery | yes |
| `ocr` | important because scan-heavy PDFs are a real part of the implementation | yes |
| `xml` | accurate because the app generates readable XML output | yes |
| `esx` | directly matches the export target and niche search intent | yes |

## Industry And Domain Topics

| Topic | Why it helps | Recommend |
| --- | --- | --- |
| `insurance` | broad domain anchor for the repo | yes |
| `insurance-claims` | more specific to the workflow context than `insurance` alone | yes |
| `property-claims` | narrows the domain toward restoration/property estimate work | yes |
| `xactimate` | important because many users will search from the Xactimate/ESX angle | yes |
| `estimate-parser` | communicates that the repo is tuned for estimate documents, not generic PDFs | yes |
| `estimate` | understandable to industry users, but broader and less precise than `estimate-parser` | optional |
| `roofing` | the app can extract roof-related measurements, but roofing is not the whole product | no |

## Technical Implementation Topics

| Topic | Why it helps | Recommend |
| --- | --- | --- |
| `desktop-app` | accurate because this is a local Windows GUI application | yes |
| `python` | important baseline topic for contributor discovery | yes |
| `pyinstaller` | useful because packaged Windows delivery is part of the repo story now | yes |
| `claims-automation` | stronger and more specific than generic `automation` | yes |
| `automation` | true, but too generic compared with `claims-automation` | no |

## Optional Stretch Or Niche Topics

| Topic | Why it helps | Recommend |
| --- | --- | --- |
| `pdf-to-xml` | technically true, but the repo is more specific than a generic PDF-to-XML transformer | optional |
| `xactimate-esx` | niche but very targeted if that topic exists in GitHub search behavior for the audience | optional |
| `estimate-conversion` | understandable, but less standard than the chosen core/domain topics | optional |
| `insurance-tech` | broad and somewhat marketing-heavy; useful only if the maintainer wants wider startup/insurtech discovery | optional |

## Recommended Final Topic Set

Recommended final topic list for the GitHub repository:

1. `pdf`
2. `pdf-parser`
3. `data-extraction`
4. `document-processing`
5. `ocr`
6. `xml`
7. `esx`
8. `xactimate`
9. `insurance`
10. `insurance-claims`
11. `property-claims`
12. `estimate-parser`
13. `claims-automation`
14. `desktop-app`
15. `python`
16. `pyinstaller`

## Optional Add-On Topics If The Maintainer Wants A Wider Reach

Consider adding one or two of these only if the topic list still feels too narrow:

- `pdf-to-xml`
- `xactimate-esx`
- `insurance-tech`

## Topics To Avoid Right Now

- `roofing`
  the app has some roof-measurement handling, but the repo is broader than roofing software
- `automation`
  too generic compared with `claims-automation`
- topics that imply enterprise SaaS, cloud AI, or broad insurer integrations
  those would misrepresent the current project

## Related Docs

- [REPO_DESCRIPTION_OPTIONS.md](./REPO_DESCRIPTION_OPTIONS.md)
- [PUBLIC_POSITIONING.md](./PUBLIC_POSITIONING.md)
- [GITHUB_REPO_SETTINGS_CHECKLIST.md](./GITHUB_REPO_SETTINGS_CHECKLIST.md)
