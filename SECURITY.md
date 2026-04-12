# Security Policy

## Reporting A Vulnerability

Do not open public GitHub issues for suspected security vulnerabilities.

Preferred path:

1. use GitHub Private Vulnerability Reporting for the public repository if it is enabled
2. if that private reporting path is not yet enabled on the hosted repository, contact the maintainer privately through the repository owner's GitHub profile or organization contact path

When reporting:

- include the affected version or commit if known
- include reproduction details
- include impact assessment
- avoid posting exploit details publicly before review

## What Belongs In Security Reporting

Use this path for issues such as:

- arbitrary file write or overwrite
- path traversal
- unsafe archive handling
- code execution from crafted input
- dependency vulnerabilities with real project impact
- unsafe handling of secrets or credentials if the project later adds them

## What Does Not Belong In Security Reporting

Use normal issue templates for:

- parser misses or unsupported layouts
- incorrect field extraction
- XML or `.esx` compatibility mismatches without a security dimension
- setup trouble
- feature requests
- documentation bugs

See [SUPPORT.md](SUPPORT.md) for the normal support paths.

## Supported Versions

The project is pre-`1.0.0`.

Security fixes should target:

- the default branch
- the latest tagged release once public releases begin

## Maintainer Note

Before broad public promotion, maintainers should enable GitHub Private Vulnerability Reporting and keep this file aligned with the actual private reporting path.
