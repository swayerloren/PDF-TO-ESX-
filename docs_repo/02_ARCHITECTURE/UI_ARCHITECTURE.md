# UI Architecture

## Main UI File

The desktop UI is implemented in `src/pdf_to_esx_agent/ui/main_window.py`.

It is a Tk-based app with optional drag-and-drop support through `tkinterdnd2`.

## UI Responsibilities

- collect PDF files
- collect the output folder
- prevent obvious invalid actions
- run conversion work on a background thread
- present progress, preview, validation, and success/error states

## Deliberate UI Boundaries

The UI does not perform parsing or XML generation itself.

It delegates conversion work to `ConversionService` and focuses on operator-facing state:

- selected files
- current status text
- state banner color and message
- log text
- validation panel
- preview panel

## Threading Model

The app keeps the Tk event loop responsive by launching conversion on a worker thread, pushing progress and result events through a queue, and polling that queue from the UI thread.

## Success And Failure Handling

Clear states are intentional:

- no files selected
- conversion running
- success
- success with warnings
- failure with visible error text

`ConversionError` is surfaced as a user-facing problem rather than as a raw traceback dialog.

## Why The UI Is Intentionally Simple

The hard problem in this repo is the data pipeline, not widget complexity. The UI exists to make that pipeline usable and debuggable.
