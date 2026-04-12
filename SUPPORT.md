# Support

This repository is open-source software. It is documented for contributors and users, but it does not promise private one-on-one support.

## Where To Go

| Need | Best path |
| --- | --- |
| setup help | start with [README.md](README.md) and [docs_repo/00_START_HERE/QUICK_START_FOR_DEVELOPERS.md](docs_repo/00_START_HERE/QUICK_START_FOR_DEVELOPERS.md) |
| general bug report | use the GitHub `bug_report` issue template |
| parser problem or unsupported estimate layout | use the GitHub `parser_layout_support` issue template |
| ESX/XML output problem | use the GitHub `esx_output_problem` issue template |
| feature idea | use the GitHub `feature_request` issue template |
| contributor guidance | read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs_repo/06_CONTRIBUTING/](docs_repo/06_CONTRIBUTING/) |
| security concern | follow [SECURITY.md](SECURITY.md) and do not post it publicly |
| conduct concern | contact the maintainers privately through the repository owner's GitHub profile or organization contact path, and do not open a public issue |

## Before Opening An Issue

Please gather as much of the following as you can:

- app version or commit hash
- operating system
- whether the PDF is mostly text-based or scanned
- whether OCR was used
- relevant log excerpts from `logs/pdf_to_esx_agent.log`
- the generated `*.canonical.json` and `*.esx.xml` if safe to share
- exact expected behavior versus actual behavior

## Sensitive Document Rule

Do not upload unredacted claim documents, personal information, policy information, or other private data to public issues.

If you cannot share the PDF, describe:

- carrier or estimate style
- whether it is scanned
- which fields failed
- which pages failed
- what the canonical and XML output looked like
