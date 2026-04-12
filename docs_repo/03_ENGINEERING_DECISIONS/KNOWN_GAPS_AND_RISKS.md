# Known Gaps And Risks

## Current Gaps

- native proprietary ESX packing is not implemented
- OCR-heavy layouts still produce incomplete names, addresses, or totals in some cases
- line-item parsing remains the most fragile subsystem
- automated tests cover important seams, but not a broad matrix of fixture PDFs

## Main Technical Risks

| Risk | Why it matters |
| --- | --- |
| parser overfitting to a few fixtures | could improve one carrier while regressing another |
| export assumptions drifting from real ESX expectations | could produce structurally valid XML that still lacks desired compatibility |
| weak fixture coverage | regressions may not be detected early |
| hidden UI coupling | future UI feature work could accidentally bypass `ConversionService` |

## Current Mitigations

- canonical boundary before export
- post-write package validation
- real multi-layout PDF validation already performed
- documented limitations instead of pretending coverage is complete
