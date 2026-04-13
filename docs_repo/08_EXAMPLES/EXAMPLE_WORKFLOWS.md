# Example Workflows

## Workflow 1: Convert One Estimate

1. Launch the app.
2. Add one estimate PDF.
3. Choose the output folder.
4. Click `Convert To ESX`.
5. Review the preview and validation panel.
6. Open the generated `.esx`, `.esx.xml`, and `.canonical.json`.

## Workflow 2: Merge Related PDFs

1. Launch the app.
2. Add multiple PDFs that belong to the same estimate packet.
3. Convert.
4. Inspect warnings for metadata conflicts or duplicate line-item removal.
5. Use the merged canonical/export artifacts.

## Workflow 3: Debug A Weak Parse

1. Run one problematic PDF.
2. Inspect the runtime log file.
   Source mode: `logs/pdf_to_esx_agent.log`
   Packaged mode: `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`
3. Inspect `*.canonical.json`.
4. Determine whether the issue belongs to ingestion, extraction, merge, or export.
5. Add a targeted code change and a regression test.
