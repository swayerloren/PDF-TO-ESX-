# Windows EXE Build

## Packaging Approach

This project uses PyInstaller with a checked-in spec file:

- spec file: `PDF-TO-ESX-Agent.spec`
- build scripts:
  - `scripts\Build-Windows-Exe.ps1`
  - `scripts\Build-Windows-Exe.bat`
- packaged output:
  - `dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`

The current build uses `onedir`, not `onefile`.

The build script also removes transient `build\pyinstaller\` output after a successful build and strips packaging metadata directories such as `*.dist-info` from the release folder.

## Why `onedir` Was Chosen

`onedir` is the safer choice for the current stack because the app depends on:

- `tkinter`
- `tkinterdnd2`
- local OCR assets from `rapidocr_onnxruntime`
- `onnxruntime` native libraries

`onefile` adds startup extraction behavior and more brittle asset resolution for this combination. `onedir` produces a cleaner and more reliable frozen runtime for a desktop tool that outside users can unzip and launch.

## Executable Target

The packaged executable targets `run_app.py`.

That entrypoint was chosen because:

- it already matches the normal source launch flow
- it wires `src\` onto `sys.path` cleanly in source mode
- it delegates to `pdf_to_esx_agent.app.bootstrap.main`
- it is the same startup path used by `scripts\Run-App.ps1`

## Frozen-Mode Runtime Behavior

The app now distinguishes between source mode and frozen mode in `src/pdf_to_esx_agent/core/settings.py`.

| Area | Source mode | Frozen mode |
| --- | --- | --- |
| executable entry | `python run_app.py` | `PDF-TO-ESX-Agent.exe` |
| logs | `logs\pdf_to_esx_agent.log` | `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log` |
| default output root | `sample_output\generated\` | `%USERPROFILE%\Documents\PDF TO ESX AGENT\generated\` |
| repo/doc paths | repo-relative | executable-relative for bundled files |

This split avoids writing logs into the extracted or installed app directory in packaged mode.

The packaged app also keeps logging file-only in frozen mode. That avoids meaningless console-stream setup for the normal GUI launch path.

## Build Commands

Recommended:

```powershell
.\scripts\Build-Windows-Exe.ps1
```

Execution-policy-safe wrapper:

```bat
scripts\Build-Windows-Exe.bat
```

Manual equivalent:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --distpath dist --workpath build\pyinstaller PDF-TO-ESX-Agent.spec
```

## Included Runtime Files

The spec file explicitly carries forward the runtime pieces the app needs:

- `rapidocr_onnxruntime` model files and `config.yaml`
- `tkinterdnd2` Windows `tkdnd` runtime files
- `onnxruntime` dynamic libraries

It does not intentionally bundle development-only docs or sample-output clutter.

## Where The EXE Ends Up

Final executable:

- `dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`

Supporting runtime directory:

- `dist\PDF-TO-ESX-Agent\_internal\`

Important:

- ship the whole `dist\PDF-TO-ESX-Agent\` folder
- do not distribute only `PDF-TO-ESX-Agent.exe`

## How To Test The Packaged Build

### 1. GUI startup smoke

```powershell
.\dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe
```

Expected result:

- the UI opens
- no console window appears
- no immediate startup crash occurs
- a packaged launch should not create a new `conhost.exe`

### 2. Real packaged conversion smoke

The frozen app includes a maintainer-facing validation path:

```powershell
& ".\dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe" --headless-convert "C:\Path\To\Estimate.pdf" --output-dir "$env:TEMP\pdf-to-esx-agent-packaged-convert"
```

Expected result:

- generated `*.esx`
- generated `*.esx.xml`
- generated `*.canonical.json`
- logs written to `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`

This mode exists for release validation. Normal end users should launch the GUI without arguments.

Because the packaged app is built as a windowed executable, some shells do not surface its exit code reliably. Treat the generated artifacts and packaged log entries as the primary success signal.

## Validation Completed In This Repo

On April 12, 2026, the packaged build was validated with:

- successful PyInstaller `onedir` build
- GUI startup smoke from `dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`
- copied-release-folder validation from `C:\Users\LJ\AppData\Local\Temp\PDF TO ESX AGENT Clean Release Validation\PDF-TO-ESX-Agent`
- no new `conhost.exe` process observed during packaged GUI launch
- real packaged conversion against `Statefarm estimate.pdf`
- real packaged conversion from a copied temp release folder with spaces in the path
- default packaged output verified under `%USERPROFILE%\Documents\PDF TO ESX AGENT\generated\`
- confirmed output creation for `.esx`, `.esx.xml`, and `.canonical.json`
- confirmed packaged-mode logging under `%LOCALAPPDATA%`

## Troubleshooting

### Missing import or startup failure in packaged mode

Check:

- `PDF-TO-ESX-Agent.spec`
- `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`
- whether the missing package needs explicit `collect_submodules`, `collect_data_files`, or `collect_dynamic_libs`

### OCR works in source mode but not packaged mode

Check:

- bundled `rapidocr_onnxruntime` model files under `dist\PDF-TO-ESX-Agent\_internal\`
- packaged logs for OCR initialization errors
- whether the spec still includes `config.yaml` and `models/*.onnx`

### Drag and drop fails only in the packaged build

Check:

- bundled `tkinterdnd2` runtime files under `dist\PDF-TO-ESX-Agent\_internal\tkinterdnd2\`
- whether the spec still includes `tkdnd/win-x64/*`

### Logs still appear repo-relative in packaged mode

Check:

- `src/pdf_to_esx_agent/core/settings.py`
- whether `sys.frozen` is detected correctly
- whether Windows known-folder lookup or `%LOCALAPPDATA%` fallback resolved correctly

### PowerShell blocks build scripts

Use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Build-Windows-Exe.ps1
```

or:

```bat
scripts\Build-Windows-Exe.bat
```

## Known Packaging Limitations

- The build is Windows-only.
- The current artifact is a zipped `onedir` app, not an installer.
- The app icon and signed executable metadata are not implemented yet.
- The packaged validation path is maintainer-oriented and not intended as the normal user workflow.
- Some shells do not report a useful process exit code for the windowed validation mode.

## Related Files

- [README.md](../README.md)
- [FINAL_BUILD_STATUS.md](./FINAL_BUILD_STATUS.md)
- [PACKAGED_APP_VALIDATION.md](./PACKAGED_APP_VALIDATION.md)
- [../docs_repo/06_CONTRIBUTING/DEVELOPMENT_SETUP.md](../docs_repo/06_CONTRIBUTING/DEVELOPMENT_SETUP.md)
- [../docs_repo/09_RELEASE_AND_OPEN_SOURCE/GITHUB_RELEASE_CHECKLIST.md](../docs_repo/09_RELEASE_AND_OPEN_SOURCE/GITHUB_RELEASE_CHECKLIST.md)
