# Config Reference

## Runtime Settings Source

Runtime settings are defined in `src/pdf_to_esx_agent/core/settings.py`.

## Current Settings

| Setting | Meaning |
| --- | --- |
| `app_title` | window title and app name |
| `repo_root` | detected repository root |
| `docs_dir` | `docs/` path |
| `logs_dir` | `logs/` path |
| `sample_output_dir` | `sample_output/` path |
| `default_output_dir` | `sample_output/generated/` |
| `debug` | enabled by `PDF_TO_ESX_DEBUG` |

## Environment Variables

| Variable | Effect |
| --- | --- |
| `PDF_TO_ESX_DEBUG` | enables debug logging when set to truthy values such as `1`, `true`, `yes`, or `on` |

## Current Philosophy

Configuration is intentionally light. The repo does not currently use a large external config system because the workflow is local and narrow.
