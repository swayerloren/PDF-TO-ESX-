from __future__ import annotations

from dataclasses import dataclass, field
import io
import logging
import re
from typing import Any

from pypdf import PdfReader

from pdf_to_esx_agent.core.numbers import extract_money_tokens
from pdf_to_esx_agent.core.text import normalize_multiline_text
from pdf_to_esx_agent.ocr.rapid_ocr import OcrLine, OcrSegment, PdfOcrExtractor


@dataclass(frozen=True)
class DocumentPage:
    page_number: int
    text: str
    lines: list[str]
    ocr_used: bool = False
    ocr_lines: tuple[OcrLine, ...] = ()
    ocr_segments: tuple[OcrSegment, ...] = ()
    text_source: str = "native_pdf_text"
    scan_classification: str = "native"
    ocr_quality_score: float = 0.0
    ocr_table_rows: int = 0
    ocr_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LoadedDocument:
    file_name: str
    pages: list[DocumentPage]
    full_text: str
    errors: list[str] = field(default_factory=list)
    ocr_attempted: bool = False
    ocr_used: bool = False
    scan_classification: str = "native"
    text_source: str = "native_pdf_text"
    ocr_quality_score: float = 0.0
    routed_page_count: int = 0
    ocr_page_count: int = 0
    scan_pipeline_status: str = "not_needed"

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def readable_page_count(self) -> int:
        return sum(1 for page in self.pages if page.text.strip())

    @property
    def extracted_text_char_count(self) -> int:
        return sum(len(page.text.strip()) for page in self.pages)

    @property
    def has_readable_text(self) -> bool:
        return self.extracted_text_char_count > 0

    @property
    def extraction_failure_reason(self) -> str | None:
        if not self.pages:
            return "PDF could not be parsed into readable pages."
        if not self.has_readable_text:
            if self.errors:
                return "PDF text extraction failed before readable text was available."
            return "PDF did not yield readable text."
        return None


class DocumentLoader:
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger("pdf_to_esx_agent").getChild("document_loader")
        self._ocr = PdfOcrExtractor(logger=self._logger.getChild("ocr"))

    def load_pdf_bytes(self, file_name: str, payload: bytes) -> LoadedDocument:
        errors: list[str] = []
        try:
            reader = PdfReader(io.BytesIO(payload))
        except Exception as exc:
            self._logger.exception("[load] Failed to load PDF %s", file_name)
            return LoadedDocument(file_name=file_name, pages=[], full_text="", errors=[str(exc)])

        raw_pages: list[DocumentPage] = []
        page_assessments: dict[int, dict[str, Any]] = {}
        routed_pages: set[int] = set()

        for page_index, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:
                errors.append(f"Page {page_index}: {exc}")
                text = ""
            try:
                image_count = len(list(page.images))
            except Exception:
                image_count = 0

            normalized = normalize_multiline_text(text)
            lines = [line.strip() for line in normalized.splitlines() if line.strip()]
            assessment = _assess_page_for_scan_pipeline(normalized, lines, image_count=image_count)
            page_assessments[page_index] = assessment
            if assessment["routeToScanPipeline"]:
                routed_pages.add(page_index)
            raw_pages.append(
                DocumentPage(
                    page_number=page_index,
                    text=normalized,
                    lines=lines,
                    scan_classification="candidate_scan" if assessment["routeToScanPipeline"] else "native",
                    ocr_metadata={
                        "nativeCharCount": assessment["nativeCharCount"],
                        "nativeLineCount": assessment["nativeLineCount"],
                        "scanReasons": assessment["reasons"],
                    },
                )
            )

        if not routed_pages and self._ocr.is_available():
            if not any(page.text.strip() for page in raw_pages):
                routed_pages = {page.page_number for page in raw_pages}
                self._logger.warning(
                    "[ocr] Embedded text extraction produced no readable text for %s; retrying OCR on all pages.",
                    file_name,
                )

        ocr_results = self._ocr.extract_pages(file_name, payload, routed_pages) if routed_pages else {}
        pages: list[DocumentPage] = []
        ocr_used = False
        for page in raw_pages:
            replacement = ocr_results.get(page.page_number)
            assessment = page_assessments.get(page.page_number, {})
            if replacement is None:
                pages.append(page)
                continue
            native_char_count = len(page.text.strip())
            replacement_char_count = len(replacement.text.strip())
            quality_score = float(replacement.quality.get("avgScore", 0.0) or 0.0)
            prefer_ocr = (
                native_char_count < 90
                or replacement_char_count > (native_char_count * 1.2)
                or (quality_score >= 0.72 and replacement_char_count > native_char_count)
            )
            if not prefer_ocr:
                pages.append(page)
                continue
            ocr_used = True
            pages.append(
                DocumentPage(
                    page_number=page.page_number,
                    text=normalize_multiline_text(replacement.text),
                    lines=[line.strip() for line in replacement.lines if line.strip()],
                    ocr_used=True,
                    ocr_lines=replacement.ocr_lines,
                    ocr_segments=replacement.ocr_segments,
                    text_source="enhanced_scan_pipeline",
                    scan_classification="scanned",
                    ocr_quality_score=quality_score,
                    ocr_table_rows=int(replacement.quality.get("tableRowCount", 0) or 0),
                    ocr_metadata={
                        "nativeCharCount": assessment.get("nativeCharCount"),
                        "nativeLineCount": assessment.get("nativeLineCount"),
                        "scanReasons": assessment.get("reasons") or [],
                        "quality": replacement.quality,
                        "sourceVariant": replacement.source_variant,
                    },
                )
            )

        full_text = "\n".join(page.text for page in pages if page.text)
        ocr_page_count = sum(1 for page in pages if page.ocr_used)
        quality_scores = [page.ocr_quality_score for page in pages if page.ocr_quality_score > 0]
        scan_classification = _classify_document_scan(pages, page_assessments)
        if routed_pages and not self._ocr.is_available():
            pipeline_status = "unavailable"
        elif routed_pages and ocr_page_count == 0:
            pipeline_status = "degraded"
        elif ocr_page_count:
            pipeline_status = "used"
        else:
            pipeline_status = "native"
        return LoadedDocument(
            file_name=file_name,
            pages=pages,
            full_text=full_text,
            errors=errors,
            ocr_attempted=bool(routed_pages and self._ocr.is_available()),
            ocr_used=ocr_used,
            scan_classification=scan_classification,
            text_source="enhanced_scan_pipeline" if ocr_page_count else "native_pdf_text",
            ocr_quality_score=round(sum(quality_scores) / len(quality_scores), 4) if quality_scores else 0.0,
            routed_page_count=len(routed_pages),
            ocr_page_count=ocr_page_count,
            scan_pipeline_status=pipeline_status,
        )


_SUMMARY_OCR_MARKERS = (
    "summaryfor",
    "lineitemtotal",
    "materialsalestax",
    "replacementcostvalue",
    "lessdepreciation",
    "lessdeductible",
    "netactualcashvaluepayment",
    "netclaimremaining",
    "replacementcostbenefits",
)


def _needs_ocr_followup(normalized: str, lines: list[str]) -> bool:
    if len(normalized.strip()) < 40:
        return True
    compact = re.sub(r"[^a-z0-9]+", "", normalized.lower())
    if sum(marker in compact for marker in _SUMMARY_OCR_MARKERS) < 4:
        return False
    summary_lines = [line for line in lines if any(marker in re.sub(r"[^a-z0-9]+", "", line.lower()) for marker in _SUMMARY_OCR_MARKERS)]
    inline_money_lines = sum(1 for line in summary_lines if extract_money_tokens(line))
    orphan_money_lines = sum(
        1
        for line in lines
        if extract_money_tokens(line)
        and not any(marker in re.sub(r"[^a-z0-9]+", "", line.lower()) for marker in _SUMMARY_OCR_MARKERS)
    )
    return inline_money_lines <= 2 and orphan_money_lines >= 4


def _assess_page_for_scan_pipeline(normalized: str, lines: list[str], *, image_count: int) -> dict[str, Any]:
    nonempty_lines = [line for line in lines if line.strip()]
    native_char_count = len(normalized.strip())
    native_line_count = len(nonempty_lines)
    score = 0.0
    reasons: list[str] = []

    if native_char_count < 80:
        score += 0.6
        reasons.append("very_low_embedded_text")
    elif native_char_count < 180:
        score += 0.28
        reasons.append("low_embedded_text")

    if native_line_count <= 3:
        score += 0.18
        reasons.append("very_low_line_count")
    elif native_line_count <= 8:
        score += 0.08
        reasons.append("low_line_count")

    if _needs_ocr_followup(normalized, lines):
        score += 0.48
        reasons.append("fragmented_payment_or_table_text")

    average_line_length = (native_char_count / native_line_count) if native_line_count else 0.0
    if native_char_count < 220 and average_line_length < 18:
        score += 0.14
        reasons.append("short_fragment_lines")
    if image_count > 0 and native_char_count < 600:
        score += 0.10
        reasons.append("image_backed_page")

    return {
        "routeToScanPipeline": score >= 0.55,
        "scanScore": round(min(score, 1.0), 4),
        "reasons": reasons,
        "nativeCharCount": native_char_count,
        "nativeLineCount": native_line_count,
        "imageCount": image_count,
    }


def _classify_document_scan(pages: list[DocumentPage], page_assessments: dict[int, dict[str, Any]]) -> str:
    if not pages:
        return "unknown"
    routed_pages = [
        assessment
        for page_number, assessment in page_assessments.items()
        if assessment.get("routeToScanPipeline") or (page_number <= len(pages) and pages[page_number - 1].ocr_used)
    ]
    routed_ratio = len(routed_pages) / len(pages)
    if routed_ratio >= 0.6:
        return "scanned"
    if routed_ratio > 0:
        return "mixed"
    return "native"
