# Release Checklist

Use this checklist before cutting a public release or promoting a new tag heavily.

## Product Reality

- confirm the app still runs locally on Windows
- confirm README statements match the actual implementation
- confirm known limitations are still honest
- confirm ESX compatibility language is not overstated

## Validation

- run unit tests
- run `python -m compileall`
- run `.\scripts\Verify-Clean-Environment.ps1`
- run `.\scripts\Build-Windows-Exe.ps1`
- launch the packaged executable once
- run at least one real PDF conversion smoke test if local fixtures are available
- run at least one real packaged conversion smoke if local fixtures are available
- inspect the generated `*.canonical.json` and `*.esx.xml`

## Documentation And Versioning

- bump the version if needed
- update [CHANGELOG.md](CHANGELOG.md)
- update [ROADMAP.md](ROADMAP.md) if priorities changed
- update `docs_repo` docs when architecture, mapping, or contributor guidance changed
- confirm release notes and known limitations align with the code

## Open-Source Repo Assets

- confirm [LICENSE](LICENSE) is present
- confirm [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [SUPPORT.md](SUPPORT.md) are present and aligned
- confirm GitHub issue templates and PR template are present
- confirm workflows are present and still match the actual stack
- confirm repo hygiene files are present and current

## Repo Cleanliness

- confirm runtime logs are not committed accidentally
- confirm `sample_output/generated/` is clean unless an intentional example is being shipped
- confirm no unredacted customer or claim documents are being published
- confirm docs link to files that actually exist
