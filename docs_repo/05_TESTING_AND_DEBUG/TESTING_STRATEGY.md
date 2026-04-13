# Testing Strategy

## Current Testing Layers

The project currently uses three practical layers of verification:

1. unit/smoke tests in `tests/`
2. clean-environment startup verification
3. real PDF conversion runs against local fixtures
4. packaged executable build and startup/conversion smoke

## Automated Coverage Today

Current automated checks cover:

- writer/package validation smoke
- invalid PDF rejection
- missing-file rejection
- non-PDF rejection
- invalid output-folder rejection
- deterministic output naming and filename sanitization
- clean-environment install and UI startup smoke
- source-vs-frozen settings behavior

## Commands

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall src run_app.py tests
.\scripts\Verify-Clean-Environment.ps1
.\scripts\Build-Windows-Exe.ps1
```

## Real-World Validation

Real PDF validation matters more than synthetic unit tests alone because estimate layouts vary heavily by carrier and document quality.

This repo has already been validated against multiple real estimate PDFs from the source-agent fixture set, including OCR-heavy inputs.

## Highest-Value Future Test Areas

- fixture-based parser regression tests
- more line-item financial parsing cases
- more metadata extraction edge cases
- more export-compatibility assertions driven by real ESX references

## Testing Philosophy

- keep tests fast for the core contract
- use fixtures for behavior that is layout-sensitive
- validate outputs structurally, not only by file existence
