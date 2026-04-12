from __future__ import annotations

import re

from pdf_to_esx_agent.core.text import compact_text
from pdf_to_esx_agent.parsing.document_loader import DocumentPage, LoadedDocument


ITEM_START_RE = re.compile(r"^[+*]?\s*[0-9Il|\s]{1,5}[a-z]?\.(?=\s*[A-Za-z])\s*")
MONEY_SUMMARY_MARKERS = (
    "replacement cost value",
    "repair/replacement cost",
    "actual cash value",
    "net claim",
    "net actual cash value payment",
    "total acv settlement",
    "total payment amount",
    "less deductible",
    "less depreciation",
    "prior payment",
    "payment summary",
    "line of coverage",
    "recap by category",
    "award amount",
)
REPLACEMENT_BENEFIT_MARKERS = (
    "replacement cost benefits",
    "maximum additional amount available if incurred",
    "total amount of claim if incurred",
    "total paid when incurred",
    "paid when incurred",
)
GEOMETRY_MARKERS = (
    "surface area",
    "number of squares",
    "total perimeter length",
    "total ridge length",
    "total hip length",
    "eagleview",
)
EXPLANATION_MARKERS = (
    "internal information",
    "understanding your property estimate",
    "guide to reading your adjuster summary",
    "this summary guide is based on a sample estimate",
    "estimate cover page",
    "guide to understanding a property estimate",
)
SAMPLE_GUIDE_MARKERS = (
    "this summary guide is based on a sample estimate",
    "sample guide to your adjuster summary",
    "your guide to reading your adjuster summary",
    "provided for reference only",
    "reference only",
    "estimate summary guide",
    "guide to contents depreciation recovery",
    "this is a sample guide",
)
CLAIM_HEADER_MARKERS = (
    "claim number:",
    "policy number:",
    "date of loss:",
    "insured:",
    "property:",
)
PAYMENT_LETTER_MARKERS = (
    "claim outcome letter",
    "settlement breakdown",
    "additional information",
    "payment summary",
)


class PageClassifier:
    def classify(self, page: DocumentPage) -> set[str]:
        normalized = page.text.lower()
        compact = compact_text(page.text)
        page_types: set[str] = set()

        if any(marker in normalized for marker in EXPLANATION_MARKERS) or any(compact_text(marker) in compact for marker in EXPLANATION_MARKERS):
            page_types.add("explanation_only")
        if any(marker in normalized for marker in SAMPLE_GUIDE_MARKERS) or any(compact_text(marker) in compact for marker in SAMPLE_GUIDE_MARKERS):
            page_types.add("sample_guide")
        if any(marker in normalized for marker in CLAIM_HEADER_MARKERS):
            page_types.add("claim_header")
        if any(marker in normalized for marker in GEOMETRY_MARKERS):
            page_types.add("geometry")
        if any(marker in normalized for marker in REPLACEMENT_BENEFIT_MARKERS):
            page_types.add("replacement_benefits")
        if any(marker in normalized for marker in PAYMENT_LETTER_MARKERS) or any(compact_text(marker) in compact for marker in PAYMENT_LETTER_MARKERS):
            page_types.add("payment_letter")

        summary_hits = sum(marker in normalized for marker in MONEY_SUMMARY_MARKERS)
        compact_summary_hits = sum(compact_text(marker) in compact for marker in MONEY_SUMMARY_MARKERS)
        if "summary for" in normalized or "summaryfor" in compact or summary_hits >= 3 or compact_summary_hits >= 3:
            page_types.add("summary")

        line_item_count = sum(1 for line in page.lines if ITEM_START_RE.match(line.strip()))
        continued_roof_page = "continued" in normalized and ("roof" in normalized or "ro0f" in normalized or "r0of" in normalized)
        if line_item_count >= 2 or (line_item_count >= 1 and continued_roof_page):
            page_types.add("line_items")
        return page_types

    def actual_claim_pages(self, document: LoadedDocument) -> list[DocumentPage]:
        pages = [page for page in document.pages if not self.is_non_claim_page(page)]
        return pages or document.pages

    def summary_pages(self, document: LoadedDocument) -> list[DocumentPage]:
        actual_pages = self.actual_claim_pages(document)
        pages = [page for page in actual_pages if {"summary", "payment_letter", "replacement_benefits"} & self.classify(page)]
        return pages or actual_pages

    def line_item_pages(self, document: LoadedDocument) -> list[DocumentPage]:
        actual_pages = self.actual_claim_pages(document)
        pages = [page for page in actual_pages if "line_items" in self.classify(page)]
        return pages or actual_pages

    def geometry_pages(self, document: LoadedDocument) -> list[DocumentPage]:
        return [page for page in self.actual_claim_pages(document) if "geometry" in self.classify(page)]

    def is_non_claim_page(self, page: DocumentPage) -> bool:
        page_types = self.classify(page)
        if "sample_guide" in page_types:
            return True
        substantive = {"claim_header", "summary", "payment_letter", "line_items", "geometry", "replacement_benefits"}
        return "explanation_only" in page_types and not (page_types & substantive)
