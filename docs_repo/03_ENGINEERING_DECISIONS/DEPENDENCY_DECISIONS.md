# Dependency Decisions

## Runtime Dependencies

| Dependency | Why it is used |
| --- | --- |
| `pypdf` | native PDF text extraction and page access |
| `pymupdf` | rasterizing pages for OCR |
| `opencv-python` | scan preprocessing before OCR |
| `rapidocr_onnxruntime` | local OCR engine |
| `numpy` | image array processing for OCR |
| `python-dateutil` | date normalization from weak PDF text |
| `tkinterdnd2` | drag-and-drop support in the desktop UI |

## Important Constraint

OCR is optional in practice but required for best scan-heavy behavior. If OCR dependencies fail or are missing, the app still runs and surfaces the limitation through warnings.

## Dependencies Intentionally Not Used

- cloud OCR APIs
- LLM-based parsing services
- browser/Electron UI stacks
- XML schema code generation tools

These were left out to keep the app local, simple, and contributor-friendly.
