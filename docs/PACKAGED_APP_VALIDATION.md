# Packaged App Validation

## Build Date

- April 12, 2026

## Packaged Artifact Tested

- source build artifact:
  `C:\Users\LJ\Documents\PDF TO ESX AGENT\dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe`
- copied release folder used for clean-machine-like validation:
  `C:\Users\LJ\AppData\Local\Temp\PDF TO ESX AGENT Clean Release Validation\PDF-TO-ESX-Agent`

## Test Steps Performed

1. Built the release with `.\scripts\Build-Windows-Exe.ps1`.
2. Verified the build script removed transient `build\pyinstaller\` output after success.
3. Verified the packaged release folder no longer contained `*.dist-info` or `__pycache__` directories.
4. Copied the full `dist\PDF-TO-ESX-Agent\` folder to a temp path outside the repo, including spaces in the path name.
5. Launched the copied packaged executable as a GUI smoke test.
6. Checked for newly created `conhost.exe` processes during packaged GUI startup.
7. Ran a real headless packaged conversion from the copied release folder using an explicit temp output directory.
8. Verified the packaged run wrote `*.esx`, `*.esx.xml`, and `*.canonical.json`.
9. Verified packaged logging under `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`.
10. Ran a second real packaged conversion from the copied release folder without `--output-dir`.
11. Verified the default packaged output path resolved to `%USERPROFILE%\Documents\PDF TO ESX AGENT\generated\`.

## Test Results

### Build Hygiene

- `.\scripts\Build-Windows-Exe.ps1` completed successfully.
- `build\pyinstaller\` was removed after the build.
- the release folder did not contain `*.dist-info` or `__pycache__` directories after cleanup.

### GUI Launch

- the copied packaged executable launched successfully from a temp path outside the repo.
- the process remained alive during startup smoke testing.
- no new `conhost.exe` process was observed during packaged GUI launch.
- result: no evidence of a console flash on normal packaged launch.

### Real Conversion With Explicit Output Directory

Input fixture used:

- `Packaged Validation Statefarm estimate.pdf`

Output directory used:

- `%TEMP%\pdf-to-esx-agent-packaged-clean-output`

Generated files:

- `Packaged Validation Statefarm estimate.esx`
- `Packaged Validation Statefarm estimate.esx.xml`
- `Packaged Validation Statefarm estimate.canonical.json`

Result:

- conversion succeeded
- XML and `.esx` package validation succeeded
- packaged logging recorded the full parse/merge/export sequence

### Real Conversion With Default Packaged Output Path

Input fixture used:

- `Default Path Validation Statefarm estimate.pdf`

Default packaged output path observed:

- `C:\Users\LJ\Documents\PDF TO ESX AGENT\generated\`

Generated files:

- `Default Path Validation Statefarm estimate.esx`
- `Default Path Validation Statefarm estimate.esx.xml`
- `Default Path Validation Statefarm estimate.canonical.json`

Result:

- conversion succeeded
- packaged default output path is user-friendly and user-writable
- the validation artifacts created during this check were removed afterward to keep the environment tidy

### Logging

Observed packaged log file:

- `C:\Users\LJ\AppData\Local\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`

Result:

- packaged runs wrote logs to the expected LocalAppData location
- the log captured validation, parsing, merge, export, and completion messages
- frozen-mode logging stayed file-based rather than relying on a console stream

## What Still Needs Improvement Before Broad Public Distribution

- add an installer or a clearer end-user release zip process around the `onedir` folder
- add code signing for better Windows trust and download experience
- optionally add version metadata and app icon polish to the executable
- validate the packaged build on a second Windows machine outside the current development environment
- continue broadening parser regression coverage before making stronger compatibility claims
- continue documenting ESX compatibility conservatively until more external import evidence exists
