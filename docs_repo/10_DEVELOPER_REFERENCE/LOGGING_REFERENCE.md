# Logging Reference

## Main Log File

- source mode: `logs/pdf_to_esx_agent.log`
- packaged mode: `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\pdf_to_esx_agent.log`

## Logging Setup

Logging is configured in `src/pdf_to_esx_agent/core/logging.py`.

The root logger is configured once and uses both:

- a console handler
- a file handler

Format:

`timestamp | level | logger_name | message`

The root logger is then reused by child loggers for major subsystems.

## Current Logging Pattern

Examples of stage prefixes:

- `[convert]`
- `[validate]`
- `[parse]`
- `[merge]`
- `[export]`
- `[ocr]`

Logger names typically descend from `pdf_to_esx_agent`, for example:

- `pdf_to_esx_agent`
- `pdf_to_esx_agent.conversion`
- `pdf_to_esx_agent.conversion.parser`
- `pdf_to_esx_agent.conversion.export`

## What Gets Logged

- startup
- file validation
- output-folder selection
- PDF load and scan classification
- OCR activity
- parsed totals
- export generation
- package validation
- unhandled exceptions

## Where To Read Logs During Debugging

| Problem | Best signal |
| --- | --- |
| user selected a bad path | `[validate]` entries from `ConversionService` |
| a PDF opened but produced weak text | `[parse]` and `[ocr]` entries plus `*.canonical.json` |
| a merge warning surprised you | `[merge]` context in canonical warnings and debug notes |
| export failed after parsing succeeded | `[export]` entries and `ExportValidationError` wrapping |

## Debug Mode

Set `PDF_TO_ESX_DEBUG=1` before launch to enable debug-level logging.

Example:

```powershell
$env:PDF_TO_ESX_DEBUG = "1"
.\scripts\Run-App.ps1
```

## Related Docs

- [./ERROR_HANDLING_REFERENCE.md](./ERROR_HANDLING_REFERENCE.md)
- [../05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md](../05_TESTING_AND_DEBUG/DEBUGGING_GUIDE.md)
- [../02_ARCHITECTURE/DATA_FLOW_END_TO_END.md](../02_ARCHITECTURE/DATA_FLOW_END_TO_END.md)
- [../../docs/WINDOWS_EXE_BUILD.md](../../docs/WINDOWS_EXE_BUILD.md)
