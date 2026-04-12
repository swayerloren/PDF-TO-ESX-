# Product Vision

## Vision

Build an open, local-first estimate conversion tool that turns messy insurance estimate PDFs into structured export artifacts that other systems and workflows can consume.

## Practical Product Direction

The project is intentionally narrow:

- ingest insurance estimate PDFs
- recover as much structured estimate data as reasonably possible
- normalize the result into a stable internal model
- emit deterministic export artifacts

It is not trying to become a full claims platform, a document management suite, or a cloud AI parsing service.

## Why That Focus Matters

Estimate parsing is noisy enough on its own. Keeping the scope narrow helps the project stay understandable and maintainable:

- parsing logic stays local and inspectable
- contributors can reason about data quality problems more directly
- export fidelity can improve without UI and parser layers becoming tightly coupled

## Long-Term Vision

Over time, the project should become:

- a reliable open-source reference implementation for PDF-to-estimate normalization
- a contributor-friendly parser framework for new carrier layouts
- a replaceable export foundation where ESX fidelity can improve independently of parsing improvements

## Success Criteria

- outside developers can run the app quickly
- contributors can add parser rules without re-learning the entire codebase
- the canonical model remains stable as parsing heuristics evolve
- export output remains deterministic and validated
