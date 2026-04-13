# Config Reference

## Runtime Settings Source

Runtime settings are defined in `src/pdf_to_esx_agent/core/settings.py`.

## Current Settings

| Setting | Meaning |
| --- | --- |
| `app_title` | window title and app name |
| `app_slug` | packaged app/build slug |
| `repo_root` | source repo root in source mode, executable directory in frozen mode |
| `runtime_root` | repo root in source mode, `%LOCALAPPDATA%\PDF-TO-ESX-Agent` in frozen mode |
| `docs_dir` | `docs/` path under the current repo or bundle root |
| `logs_dir` | source-mode `logs/` path or frozen-mode `%LOCALAPPDATA%\PDF-TO-ESX-Agent\logs\` |
| `output_root` | source-mode `sample_output/` path or frozen-mode `%USERPROFILE%\Documents\PDF TO ESX AGENT\` |
| `default_output_dir` | `output_root/generated/` |
| `debug` | enabled by `PDF_TO_ESX_DEBUG` |
| `frozen` | true when running from the packaged executable |

## Environment Variables

| Variable | Effect |
| --- | --- |
| `PDF_TO_ESX_DEBUG` | enables debug logging when set to truthy values such as `1`, `true`, `yes`, or `on` |
| `LOCALAPPDATA` | used for frozen-mode runtime logs |
| `USERPROFILE` | used for frozen-mode default output under `Documents` |

## Current Philosophy

Configuration is intentionally light. The repo does not currently use a large external config system because the workflow is local and narrow.

Runtime-path branching exists because the packaged executable should not depend on write access to its own installation folder.
