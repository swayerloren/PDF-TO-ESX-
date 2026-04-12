from __future__ import annotations

import re

from pdf_to_esx_agent.models.estimate import EstimateLineItem, RoofMeasurements
from pdf_to_esx_agent.parsing.document_loader import LoadedDocument
from pdf_to_esx_agent.parsing.page_classifier import PageClassifier


VALUE_PATTERNS = {
    "surface_area_sq_ft": re.compile(r"([0-9][\d,]*\.\d{2})\s+Surface Area", re.IGNORECASE),
    "squares": re.compile(r"([0-9][\d,]*\.\d{2})\s+Number of Squares", re.IGNORECASE),
    "perimeter_lf": re.compile(r"([0-9][\d,]*\.\d{2})\s+Total Perimeter Length", re.IGNORECASE),
    "ridge_lf": re.compile(r"([0-9][\d,]*\.\d{2})\s+Total Ridge Length", re.IGNORECASE),
    "hip_lf": re.compile(r"([0-9][\d,]*\.\d{2})\s+Total Hip Length", re.IGNORECASE),
}


class MeasurementsExtractor:
    def __init__(self) -> None:
        self._page_classifier = PageClassifier()

    def extract(self, document: LoadedDocument, line_items: list[EstimateLineItem]) -> RoofMeasurements:
        metrics = RoofMeasurements()
        geometry_pages = self._page_classifier.geometry_pages(document)
        text = "\n".join(page.text for page in geometry_pages) if geometry_pages else document.full_text
        for field_name, pattern in VALUE_PATTERNS.items():
            match = pattern.search(text or "")
            if match:
                setattr(metrics, field_name, float(match.group(1).replace(",", "")))

        for item in line_items:
            description = item.description.lower()
            if item.quantity is None:
                continue
            if ("laminated" in description or "comp. shingle" in description or "composition shingles" in description) and item.unit == "SQ":
                metrics.squares = max(metrics.squares or 0.0, item.quantity)
            if "roofing felt" in description and item.unit == "SQ":
                metrics.felt_squares = max(metrics.felt_squares or 0.0, item.quantity)
            if "drip edge" in description and item.unit == "LF":
                metrics.drip_edge_lf = max(metrics.drip_edge_lf or 0.0, item.quantity)
            if "ice" in description and "water" in description and item.unit in {"SF", "SQ"}:
                value = item.quantity if item.unit == "SF" else item.quantity * 100.0
                metrics.ice_water_sf = max(metrics.ice_water_sf or 0.0, value)
            if "starter" in description and item.unit == "LF":
                metrics.starter_lf = max(metrics.starter_lf or 0.0, item.quantity)
            if "ridge" in description and item.unit == "LF":
                metrics.ridge_lf = max(metrics.ridge_lf or 0.0, item.quantity)
        if metrics.surface_area_sq_ft is None and metrics.squares is not None:
            metrics.surface_area_sq_ft = round(metrics.squares * 100.0, 2)
        return metrics

