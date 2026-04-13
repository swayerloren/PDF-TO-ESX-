# GitHub Repo Settings Checklist

## Purpose

This file captures the manual GitHub.com settings that should be reviewed for `PDF TO ESX AGENT`.

These are not assumptions about the current hosted repository state. They are the recommended next actions for the maintainer.

## Core Repository Presentation

| Setting | Recommendation | Why it matters |
| --- | --- | --- |
| repository description | set a short, accurate description from [REPO_DESCRIPTION_OPTIONS.md](./REPO_DESCRIPTION_OPTIONS.md) | improves search relevance and first impressions |
| homepage URL | leave blank unless a real docs site or release landing page exists | better to have no homepage than a weak or redundant one |
| topics | add the final topic set from [GITHUB_DISCOVERABILITY.md](./GITHUB_DISCOVERABILITY.md) | improves topic search discovery and repo classification |
| pinned repository | pin it on the maintainer profile if this is a priority public project | increases profile-level discoverability |

## Collaboration Settings

| Setting | Recommendation | Why it matters |
| --- | --- | --- |
| Issues | enable | the repo already has tailored issue templates and should accept public bug/parser/export reports |
| Discussions | defer for now | issue templates are a better fit than open-ended discussions at the current project scale |
| Projects | optional, only if actively maintained | a stale project board hurts credibility more than no board |
| Wiki | optional, generally not needed | `README.md` and `docs_repo/` already provide the structured knowledge base |

## Security And Trust Settings

| Setting | Recommendation | Why it matters |
| --- | --- | --- |
| Private Vulnerability Reporting | enable | aligns with `SECURITY.md` and improves responsible disclosure handling |
| Dependabot alerts | enable | useful for a Python desktop app with packaged dependencies |
| Dependabot security updates | enable if the maintainer can review them consistently | helpful, but only if they will actually be triaged |
| branch protection on `main` | recommended | protects a public repo from accidental direct pushes or unreviewed changes |

## GitHub Actions Settings

| Setting | Recommendation | Why it matters |
| --- | --- | --- |
| Actions enabled | keep enabled | workflows already validate docs, repo assets, tests, and release readiness |
| workflow permissions | prefer least privilege | read-only by default is safer until a release-publishing workflow exists |
| fork pull request workflow permissions | review carefully | useful for contributors, but should not expose unnecessary write tokens |

## Releases And Distribution

| Setting | Recommendation | Why it matters |
| --- | --- | --- |
| GitHub Releases | use for versioned milestones | the repo now has tagged milestones and packaged-build documentation |
| release assets | upload a zipped `dist\PDF-TO-ESX-Agent\` folder, not just the `.exe` | `onedir` requires the full folder to run correctly |
| release notes | derive from `CHANGELOG.md` and `PUBLIC_RELEASE_NOTES_DRAFT.md` | keeps public messaging aligned with reality |

## Visual Presentation

| Setting | Recommendation | Why it matters |
| --- | --- | --- |
| Social Preview image | add one when available | improves sharing previews and general polish |
| social preview message | follow [GITHUB_SOCIAL_PREVIEW_PLAN.md](./GITHUB_SOCIAL_PREVIEW_PLAN.md) | keeps the visual message credible and accurate |

## Recommended Manual Setup Order

1. set repository description
2. add recommended GitHub Topics
3. enable Issues if not already enabled
4. enable Private Vulnerability Reporting
5. review Actions permissions
6. decide whether to pin the repo on the maintainer profile
7. add a Social Preview image
8. use GitHub Releases for the next packaged milestone

## Settings To Avoid Rushing

- Discussions
  add only if there is enough community traffic to justify moderation
- Projects
  add only if the maintainer wants to visibly manage roadmap work in GitHub
- homepage URL
  add only when there is a real release/download or documentation landing page worth linking

## Related Docs

- [GITHUB_DISCOVERABILITY.md](./GITHUB_DISCOVERABILITY.md)
- [GITHUB_SOCIAL_PREVIEW_PLAN.md](./GITHUB_SOCIAL_PREVIEW_PLAN.md)
- [REPO_DESCRIPTION_OPTIONS.md](./REPO_DESCRIPTION_OPTIONS.md)
