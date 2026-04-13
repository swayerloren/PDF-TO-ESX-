# Tradeoffs And Constraints

## Local-First Processing

Benefit:

- no cloud dependency
- easier privacy story
- easier offline debugging

Cost:

- OCR quality is limited by local dependencies and document quality
- there is no remote fallback model

## Tk Desktop UI

Benefit:

- simple deployment for a Python project
- low complexity for a utility-style app

Cost:

- still not an installer or signed native desktop release
- packaged distribution currently ships as a PyInstaller `onedir` folder
- UI testing remains lighter than web-app tooling

## Heuristic Parsing

Benefit:

- fully inspectable
- deterministic
- easy to tune incrementally

Cost:

- carrier coverage is never "done"
- some layouts still require manual improvement over time

## Standards-Based ESX Packaging

Benefit:

- readable and testable
- easy to validate

Cost:

- not the same as a proprietary native `XACTDOC.ZIPXML` implementation
