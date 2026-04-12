# Pull Request Guidelines

## What A Good PR Looks Like

- one clear purpose
- scoped changes
- matching tests or validation notes
- updated docs when behavior changes
- explicit mention of limitations or assumptions when relevant

## PR Description Should Include

| Topic | What to say |
| --- | --- |
| what changed | summarize the concrete behavior change |
| why it changed | describe the problem being solved |
| pipeline stage | note whether the change affects ingestion, parsing, canonical merge, export, or UI |
| validation | list commands, tests, or real-fixture checks |
| risk | explain what might still be weak or unverified |

## Parser PRs Should Include

- sample layout type affected
- whether metadata, totals, or line items changed
- whether existing layouts were rechecked
- whether canonical output changed

## Export PRs Should Include

- exact XML/package change
- canonical fields affected
- whether validator rules changed
- whether output compatibility assumptions also changed

## Docs-Only PRs Should Still Be Precise

If a docs PR changes architecture, roadmap, or compatibility language, it should explain whether the docs are reflecting a code change or clarifying existing behavior only.
