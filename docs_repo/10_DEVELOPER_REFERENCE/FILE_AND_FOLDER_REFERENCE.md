# File And Folder Reference

## Source Tree

| Path | Meaning |
| --- | --- |
| `src/pdf_to_esx_agent/app/` | startup/bootstrap |
| `src/pdf_to_esx_agent/core/` | orchestration and utilities |
| `src/pdf_to_esx_agent/parsing/` | PDF loading and page classification |
| `src/pdf_to_esx_agent/ocr/` | OCR support |
| `src/pdf_to_esx_agent/extract/` | structured estimate parsing |
| `src/pdf_to_esx_agent/models/` | canonical data model |
| `src/pdf_to_esx_agent/export/` | XML/package generation |
| `src/pdf_to_esx_agent/ui/` | desktop UI |

## Project Support Folders

| Path | Meaning |
| --- | --- |
| `tests/` | automated verification |
| `scripts/` | launch, verification, and packaging helpers |
| `docs/` | implementation/build-phase documentation |
| `docs_repo/` | long-term open-source knowledge base |
| `sample_output/` | default source-mode output location |
| `logs/` | source-mode runtime logs |
| `dist/` | packaged Windows build output |
| `build/pyinstaller/` | transient PyInstaller build work directory |

## Build And Packaging Files

| Path | Meaning |
| --- | --- |
| `run_app.py` | user-facing launcher and packaged entry script |
| `PDF-TO-ESX-Agent.spec` | PyInstaller build definition |
| `requirements-build.txt` | runtime requirements plus build dependency layer |
| `scripts/Build-Windows-Exe.ps1` | primary PowerShell packaging script |
| `scripts/Build-Windows-Exe.bat` | execution-policy-safe packaging wrapper |
