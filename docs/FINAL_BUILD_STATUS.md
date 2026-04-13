# Final Build Status

## What Works Now

- The app runs from source through `run_app.py` and `.\scripts\Run-App.ps1`.
- The app also builds into a real Windows GUI executable through PyInstaller.
- The packaged artifact launches without a console window through `dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`.
- Users can add one or more estimate PDFs, choose an output folder, and convert end to end.
- Native-text PDFs and scan-heavy PDFs both flow through the same ingestion pipeline, with OCR used when text extraction is weak.
- Parsed data is normalized into a canonical estimate model before export.
- Successful runs write `*.esx`, `*.esx.xml`, and `*.canonical.json`.
- XML structure and packaged `.esx` contents are validated before success is returned to the UI.
- Common failure cases return user-facing validation messages instead of uncaught crashes.
- The packaged executable also supports a hidden validation path through `--headless-convert` so maintainers can smoke-test the frozen build with a real PDF.

## What Was Reused From SALES FORCE AGENT

- Local document-ingestion patterns for PDF-first workflows.
- OCR-routing ideas for mixed native/scanned packets.
- Separation between metadata extraction, totals extraction, line-item parsing, and normalization.
- Canonical-model boundaries so export logic stays isolated from parser heuristics.
- Logging and troubleshooting patterns appropriate for a local desktop tool.
- Real fixture PDFs and ESX/XML references used to validate the parser and export shape.

## ESX Assumptions

- The app writes a standards-based `.esx` zip package with `XACTDOC.XML`.
- The package is deterministic and structurally validated, but it is not a native proprietary `XACTDOC.ZIPXML` writer.
- The canonical estimate remains the source of truth for export.
- Missing values are omitted or left blank rather than filled with invented placeholders.
- XML escaping and numeric normalization are handled in the export layer instead of being pushed into parser logic.

## Frozen-Mode Support Added

- Runtime settings now distinguish between source mode and frozen mode.
- Frozen-mode path detection now prefers Windows known folders before environment-variable fallbacks.
- Source mode keeps logs in `logs\` and outputs in `sample_output\generated\`.
- Frozen mode keeps logs in `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\`.
- Frozen mode defaults user output to `%USERPROFILE%\Documents\PDF TO ESX AGENT\generated\`.
- The packaged app no longer creates the default output folder at startup; it is created only when needed.
- Frozen-mode logging is file-only.
- The UI now points users to the correct runtime log file when failures occur.
- A PyInstaller spec file now captures the packaging contract for OCR models, `tkinterdnd2`, and `onnxruntime`.
- The packaging script removes transient build output and strips unused metadata directories from the final bundle.

## Validation Completed On April 12, 2026

- `.\.venv\Scripts\python.exe -m compileall src run_app.py tests`
- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`
- `.\scripts\Verify-Clean-Environment.ps1`
- `.\scripts\Build-Windows-Exe.ps1`
- packaged executable startup smoke through `dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`
- packaged real conversion smoke against `Statefarm estimate.pdf`
- copied-release-folder packaged validation from a temp path with spaces

Packaged conversion artifact verified:

- `dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`
- `%TEMP%\pdf-to-esx-agent-packaged-convert\Statefarm estimate.esx`
- `%TEMP%\pdf-to-esx-agent-packaged-convert\Statefarm estimate.esx.xml`
- `%TEMP%\pdf-to-esx-agent-packaged-convert\Statefarm estimate.canonical.json`

## Exact Launch Steps

From source:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\scripts\Run-App.ps1
```

Build the Windows executable:

```powershell
.\scripts\Build-Windows-Exe.ps1
```

Launch the packaged app:

```powershell
.\dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe
```

## Future Improvement Areas

- Add more carrier-specific parsing coverage for edge-case layouts.
- Improve OCR-heavy metadata recovery on degraded scans.
- Expand totals reconciliation across more mixed summary/detail packets.
- Add installer/signing work if public end-user distribution grows beyond zipped `onedir` artifacts.
- Keep growing fixture-based regression coverage for parser and export behavior.
