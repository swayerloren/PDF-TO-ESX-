# Development Setup

## Requirements

- Windows
- Python 3.12+
- Tkinter support

## Initial Setup

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Windows Packaging Setup

Build tooling uses `requirements-build.txt`, which layers PyInstaller on top of the runtime dependencies.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
```

## Verify The Environment

| Goal | Command |
| --- | --- |
| run the app | `.\scripts\Run-App.ps1` |
| run tests | `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` |
| compile check | `.\.venv\Scripts\python.exe -m compileall src run_app.py tests` |
| clean install smoke | `.\scripts\Verify-Clean-Environment.ps1` |
| build packaged exe | `.\scripts\Build-Windows-Exe.ps1` |
| launch packaged exe | `.\dist\PDF-TO-ESX-Agent\PDF-TO-ESX-Agent.exe` |

## Useful Local Paths

| Path | Purpose |
| --- | --- |
| `src/pdf_to_esx_agent/` | application source |
| `tests/` | automated checks |
| `docs/` | implementation-focused build docs |
| `docs_repo/` | long-term project knowledge base |
| `PDF-TO-ESX-Agent.spec` | PyInstaller build contract |
| `dist/PDF-TO-ESX-Agent/` | packaged Windows build output |
| `sample_output/generated/` | default source-mode output folder |
| `%USERPROFILE%\Documents\PDF TO ESX AGENT\generated\` | default packaged-mode output folder |
| `logs/pdf_to_esx_agent.log` | source-mode runtime log file |
| `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log` | packaged-mode runtime log file |

## Common Setup Problems

| Problem | What to check |
| --- | --- |
| `py` not found | confirm Python launcher is installed |
| UI does not open | confirm Tkinter support in the Python install |
| scan-heavy PDFs parse weakly | confirm OCR dependencies installed from `requirements.txt` |
| clean-environment script fails | read the script output before changing code; the problem may be environment-only |
| build script blocked in PowerShell | use `scripts\Build-Windows-Exe.bat` or `powershell -ExecutionPolicy Bypass -File .\scripts\Build-Windows-Exe.ps1` |
| packaged app starts but cannot parse | inspect `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log` and verify the spec still includes OCR assets |

## Read Next

- [CODEBASE_TOUR.md](./CODEBASE_TOUR.md)
- [../05_TESTING_AND_DEBUG/TESTING_STRATEGY.md](../05_TESTING_AND_DEBUG/TESTING_STRATEGY.md)
- [../../docs/WINDOWS_EXE_BUILD.md](../../docs/WINDOWS_EXE_BUILD.md)
