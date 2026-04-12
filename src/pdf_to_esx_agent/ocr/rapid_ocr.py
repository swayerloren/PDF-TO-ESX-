from __future__ import annotations

from dataclasses import dataclass, field
import logging
import statistics
from typing import Any

from pdf_to_esx_agent.core.numbers import extract_money_tokens


@dataclass(frozen=True)
class OcrSegment:
    text: str
    score: float
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def center_y(self) -> float:
        return (self.y0 + self.y1) / 2

    @property
    def height(self) -> float:
        return max(self.y1 - self.y0, 0.0)


@dataclass(frozen=True)
class OcrLine:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    segments: tuple[OcrSegment, ...]


@dataclass(frozen=True)
class OcrPageResult:
    text: str
    lines: tuple[str, ...]
    ocr_lines: tuple[OcrLine, ...]
    ocr_segments: tuple[OcrSegment, ...]
    quality: dict[str, Any] = field(default_factory=dict)
    source_variant: str = "rendered"


class PdfOcrExtractor:
    def __init__(
        self,
        *,
        logger: logging.Logger | None = None,
        render_scale: float = 1.7,
        min_score: float = 0.45,
    ) -> None:
        self._logger = logger or logging.getLogger("pdf_to_esx_agent").getChild("ocr")
        self._render_scale = render_scale
        self._min_score = min_score

    def is_available(self) -> bool:
        try:
            import cv2  # noqa: F401
            import fitz  # noqa: F401
            import numpy  # noqa: F401
            from rapidocr_onnxruntime import RapidOCR  # noqa: F401
        except Exception:
            return False
        return True

    def extract_pages(self, file_name: str, payload: bytes, page_numbers: set[int]) -> dict[int, OcrPageResult]:
        if not page_numbers or not self.is_available():
            return {}

        try:
            import cv2
            import fitz
            import numpy
            from rapidocr_onnxruntime import RapidOCR
        except Exception:
            return {}

        try:
            document = fitz.open(stream=payload, filetype="pdf")
        except Exception:
            self._logger.exception("[ocr] Render failed for %s", file_name)
            return {}

        self._logger.info("[ocr] Running OCR for %s page(s) in %s", len(page_numbers), file_name)
        ocr = RapidOCR()
        results: dict[int, OcrPageResult] = {}
        for page_number in sorted(page_numbers):
            page_index = page_number - 1
            if page_index < 0 or page_index >= len(document):
                continue
            try:
                page = document[page_index]
                rendered = self._render_page_image(page, fitz=fitz, numpy=numpy)
                processed = self._preprocess_image(rendered, cv2=cv2, numpy=numpy)
                results[page_number] = self._best_result_for_image(
                    image_variants=[
                        ("rendered", rendered),
                        ("enhanced_preprocess", processed),
                    ],
                    ocr=ocr,
                    cv2=cv2,
                )
                self._logger.info("[ocr] Page %s complete for %s", page_number, file_name)
            except Exception:
                self._logger.exception("[ocr] Failed for %s page %s", file_name, page_number)
        return results

    def _render_page_image(self, page, *, fitz, numpy) -> Any:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(self._render_scale, self._render_scale), alpha=False)
        channels = max(1, int(getattr(pixmap, "n", 3) or 3))
        image = numpy.frombuffer(pixmap.samples, dtype=numpy.uint8)
        image = image.reshape(pixmap.height, pixmap.width, channels)
        if channels == 1:
            return image
        return image[:, :, :3]

    def _preprocess_image(self, image: Any, *, cv2, numpy) -> Any:
        if len(getattr(image, "shape", ())) == 2:
            grayscale = image
        else:
            grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast = clahe.apply(grayscale)
        denoised = cv2.medianBlur(contrast, 3)
        thresholded = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            11,
        )
        return cv2.filter2D(
            thresholded,
            ddepth=-1,
            kernel=numpy.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
        )

    def _best_result_for_image(self, *, image_variants: list[tuple[str, Any]], ocr, cv2) -> OcrPageResult:
        best = OcrPageResult(text="", lines=(), ocr_lines=(), ocr_segments=(), quality={})
        best_score = -1.0
        for variant_name, image in image_variants:
            ok, encoded = cv2.imencode(".png", image)
            if not ok:
                continue
            raw_result, _ = ocr(encoded.tobytes())
            result = self._build_page_result(raw_result or [], source_variant=variant_name)
            score = self._score_result(result)
            if score > best_score:
                best = result
                best_score = score
        return best

    def _build_page_result(
        self,
        raw_result: list[tuple[object, str, float]],
        *,
        source_variant: str,
    ) -> OcrPageResult:
        segments: list[OcrSegment] = []
        for item in raw_result:
            if len(item) != 3:
                continue
            raw_box, raw_text, raw_score = item
            text = str(raw_text or "").strip()
            score = float(raw_score or 0.0)
            if not text or score < self._min_score:
                continue
            try:
                xs = [float(point[0]) for point in raw_box]
                ys = [float(point[1]) for point in raw_box]
            except Exception:
                continue
            segments.append(
                OcrSegment(
                    text=text,
                    score=score,
                    x0=min(xs),
                    y0=min(ys),
                    x1=max(xs),
                    y1=max(ys),
                )
            )

        if not segments:
            return OcrPageResult(
                text="",
                lines=(),
                ocr_lines=(),
                ocr_segments=(),
                quality={"avgScore": 0.0, "segmentCount": 0, "lineCount": 0, "charCount": 0, "tableRowCount": 0},
                source_variant=source_variant,
            )

        segments.sort(key=lambda item: (item.center_y, item.x0))
        median_height = statistics.median(segment.height for segment in segments)
        row_tolerance = max(8.0, min(18.0, median_height * 0.6))
        rows: list[list[OcrSegment]] = []
        for segment in segments:
            if not rows:
                rows.append([segment])
                continue
            current = rows[-1]
            current_y = sum(item.center_y for item in current) / len(current)
            if abs(segment.center_y - current_y) <= row_tolerance:
                current.append(segment)
            else:
                rows.append([segment])

        ocr_lines: list[OcrLine] = []
        table_row_count = 0
        for row in rows:
            row.sort(key=lambda item: item.x0)
            parts: list[str] = []
            previous: OcrSegment | None = None
            wide_gaps = 0
            for segment in row:
                if previous is None:
                    parts.append(segment.text)
                    previous = segment
                    continue
                gap = segment.x0 - previous.x1
                separator = " | " if gap >= max(30.0, median_height * 1.3) else " "
                if separator == " | ":
                    wide_gaps += 1
                parts.append(f"{separator}{segment.text}")
                previous = segment
            line_text = "".join(parts).strip()
            if not line_text:
                continue
            if wide_gaps:
                table_row_count += 1
            ocr_lines.append(
                OcrLine(
                    text=line_text,
                    x0=min(segment.x0 for segment in row),
                    y0=min(segment.y0 for segment in row),
                    x1=max(segment.x1 for segment in row),
                    y1=max(segment.y1 for segment in row),
                    segments=tuple(row),
                )
            )

        line_texts = tuple(line.text for line in ocr_lines)
        joined_text = "\n".join(line_texts)
        avg_score = round(statistics.fmean(segment.score for segment in segments), 4)
        quality = {
            "avgScore": avg_score,
            "segmentCount": len(segments),
            "lineCount": len(ocr_lines),
            "charCount": len(joined_text.replace("\n", "").strip()),
            "tableRowCount": table_row_count,
            "moneyTokenCount": len(extract_money_tokens(joined_text)),
        }
        return OcrPageResult(
            text=joined_text,
            lines=line_texts,
            ocr_lines=tuple(ocr_lines),
            ocr_segments=tuple(segments),
            quality=quality,
            source_variant=source_variant,
        )

    def _score_result(self, result: OcrPageResult) -> float:
        quality = result.quality or {}
        return (
            (float(quality.get("avgScore", 0.0) or 0.0) * 300.0)
            + min(float(quality.get("charCount", 0) or 0) / 12.0, 90.0)
            + (float(quality.get("lineCount", 0) or 0) * 1.2)
            + (float(quality.get("tableRowCount", 0) or 0) * 1.5)
            + (float(quality.get("moneyTokenCount", 0) or 0) * 1.5)
        )
