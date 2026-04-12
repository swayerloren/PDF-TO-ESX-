# Final Build Status

## What Works Now

- The Windows desktop app launches from `run_app.py` or `.\scripts\Run-App.ps1`.
- Users can drag and drop or browse for one or more estimate PDFs.
- The app validates file selection and output-folder paths before conversion starts.
- Native-text PDFs and scanned/image-heavy PDFs are routed through the ingestion pipeline correctly, with OCR used when local dependencies are available.
- Parsed content is normalized into a canonical estimate model before export.
- The export layer writes `*.esx`.
- The export layer writes `*.esx.xml`.
- The export layer writes `*.canonical.json`.
- Generated XML is validated for structure and reference integrity, and the packaged `.esx` archive is validated before success is returned to the UI.
- Common failure cases now return clear user-facing errors instead of uncaught crashes.
- Missing files are rejected before conversion starts.
- Non-PDF inputs are rejected before conversion starts.
- Unreadable or broken PDFs fail through a conversion error path.
- Unusable output-folder paths fail through a conversion error path.
- Empty parses that do not contain line items or usable totals fail before export.

## What Was Reused From SALES FORCE AGENT

- Document-ingestion patterns for local file handling and PDF-first workflows.
- OCR routing concepts for mixed native/scanned documents.
- Parser organization that separates metadata extraction, totals extraction, line-item parsing, and normalization.
- Canonical-model thinking so the exporter stays isolated from raw parser heuristics.
- Logging and troubleshooting orientation suited to local agent-style desktop tools.
- Real fixture PDFs and reference ESX/XML structures used to validate parser behavior and the export shape.

## ESX Assumptions

- The app writes a standards-based `.esx` zip package with `XACTDOC.XML`, not a proprietary native `XACTDOC.ZIPXML` payload.
- `XACTDOC` is treated as the root export document based on structures observed in the source agent fixtures.
- The canonical estimate is the source of truth for export. Missing fields are omitted instead of being filled with fake placeholders.
- Line items are represented in both human-readable grouped form and compact `SUMITEM` form so the package stays inspectable and deterministic.
- Numeric fields are normalized before serialization and XML escaping is left to the XML writer.

## Future Improvement Areas

- Add more carrier-specific table parsing for edge-case line-item layouts.
- Improve OCR-heavy metadata recovery for names and addresses on degraded scans.
- Expand totals reconciliation for more payment-letter and multi-coverage packets.
- Replace the current open zip-based ESX packaging with a native proprietary packer if exact schema/packing details become available.
- Add broader automated fixture-based regression tests using a maintained local sample set.
- Package the desktop app as an installer or standalone executable if distribution becomes a requirement.

## Exact Launch Steps

From the repo root in a VS Code terminal:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\scripts\Run-App.ps1
```

Optional clean-environment verification:

```powershell
.\scripts\Verify-Clean-Environment.ps1
```

## Exact Use Steps

1. Launch the app.
2. Drag one or more insurance estimate PDFs into the upload area, or click `Add PDFs`.
3. Confirm the selected file list.
4. Choose an output folder or keep the default `sample_output\generated`.
5. Click `Convert To ESX`.
6. Watch the banner, progress bar, validation panel, and preview panel.
7. Open the output folder and use the generated `*.esx`, `*.esx.xml`, and `*.canonical.json` files.
