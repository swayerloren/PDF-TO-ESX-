# Design Decisions

## Key Decisions

| Decision | Current implementation | Why it matters |
| --- | --- | --- |
| keep the app desktop-first | Tk UI in `ui/main_window.py` | local workflows are the primary use case |
| keep processing local-first | no cloud services | predictable cost, privacy, and reproducibility |
| parse in stages | `document_loader -> extractors -> merge` | easier debugging and targeted improvements |
| normalize before export | `CanonicalEstimate` boundary | export logic stays stable as parser rules evolve |
| keep export isolated | `export/` package | ESX assumptions can change without touching ingestion |
| validate output after write | `ExportPackageValidator` | prevents silent bad exports |
| use deterministic naming | `output_stem_from_paths()` | reproducible artifacts and easier testing |

## Decisions That Shape Contributor Work

- new PDF support should usually start in `extract/` or `parsing/`, not in the UI
- new export fidelity work should usually start in `export/`, not in OCR code
- cross-cutting behavior should pass through the canonical model rather than bypass it
