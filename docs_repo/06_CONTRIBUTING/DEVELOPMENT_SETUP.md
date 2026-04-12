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

## Verify The Environment

| Goal | Command |
| --- | --- |
| run the app | `.\scripts\Run-App.ps1` |
| run tests | `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` |
| compile check | `.\.venv\Scripts\python.exe -m compileall src run_app.py tests` |
| clean install smoke | `.\scripts\Verify-Clean-Environment.ps1` |

## Useful Local Paths

| Path | Purpose |
| --- | --- |
| `src/pdf_to_esx_agent/` | application source |
| `tests/` | automated checks |
| `docs/` | implementation-focused build docs |
| `docs_repo/` | long-term project knowledge base |
| `sample_output/generated/` | default output folder at runtime |
| `logs/pdf_to_esx_agent.log` | runtime log file |

## Common Setup Problems

| Problem | What to check |
| --- | --- |
| `py` not found | confirm Python launcher is installed |
| UI does not open | confirm Tkinter support in the Python install |
| scan-heavy PDFs parse weakly | confirm OCR dependencies installed from `requirements.txt` |
| clean-environment script fails | read the script output before changing code; the problem may be environment-only |

## Read Next

- [CODEBASE_TOUR.md](./CODEBASE_TOUR.md)
- [../05_TESTING_AND_DEBUG/TESTING_STRATEGY.md](../05_TESTING_AND_DEBUG/TESTING_STRATEGY.md)
