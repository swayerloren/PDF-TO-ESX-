# Example Outputs

## Standard Output Set

One successful conversion writes:

- `<stem>.esx`
- `<stem>.esx.xml`
- `<stem>.canonical.json`

## Example Naming

Single-file conversion:

- `Statefarm estimate.esx`

Merged conversion:

- `Tripathi Allstate original scope_merged_2_files.esx`

The merged stem is deterministic and based on sorted input names, not the order the user clicked files.

## What Each Output Is For

| File | Purpose |
| --- | --- |
| `*.esx` | packaged export artifact |
| `*.esx.xml` | readable XML for inspection/debugging |
| `*.canonical.json` | normalized estimate for parser/debug work |

## Typical Success Pattern

- UI banner shows success or success-with-warnings
- validation panel lists warnings when fields were missing or recovered
- output folder contains all three artifacts
