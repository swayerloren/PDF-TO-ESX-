from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from pdf_to_esx_agent.core.numbers import ZERO, format_money


@dataclass
class ValidationMessage:
    level: str
    message: str
    context: str | None = None


@dataclass
class SourceDocument:
    file_name: str
    file_path: str
    page_count: int
    readable_page_count: int
    extracted_text_char_count: int
    scan_classification: str = "native"
    text_source: str = "native_pdf_text"
    ocr_attempted: bool = False
    ocr_used: bool = False
    ocr_page_count: int = 0
    warnings: list[str] = field(default_factory=list)


@dataclass
class EstimateMetadata:
    estimate_name: str | None = None
    estimate_number: str | None = None
    estimate_date: str | None = None
    carrier: str | None = None
    insured_name: str | None = None
    property_address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    claim_number: str | None = None
    policy_number: str | None = None
    date_of_loss: str | None = None
    date_inspected: str | None = None
    estimator_name: str | None = None
    estimator_phone: str | None = None
    estimator_email: str | None = None
    price_list_code: str | None = None
    price_list_region: str | None = None
    price_list_month: str | None = None
    price_list_year: int | None = None


@dataclass
class EstimateTotals:
    replacement_cost_value: Decimal | None = None
    actual_cash_value: Decimal | None = None
    gross_acv: Decimal | None = None
    deductible: Decimal | None = None
    depreciation: Decimal | None = None
    recoverable_depreciation: Decimal | None = None
    nonrecoverable_depreciation: Decimal | None = None
    prior_payments: Decimal | None = None
    net_payable: Decimal | None = None
    total_if_incurred: Decimal | None = None
    tax_total: Decimal | None = None
    subtotal: Decimal | None = None
    overhead_and_profit: Decimal | None = None
    line_item_total: Decimal | None = None
    grand_total: Decimal | None = None


@dataclass
class RoofMeasurements:
    surface_area_sq_ft: float | None = None
    squares: float | None = None
    perimeter_lf: float | None = None
    ridge_lf: float | None = None
    hip_lf: float | None = None
    valley_lf: float | None = None
    eaves_lf: float | None = None
    rakes_lf: float | None = None
    drip_edge_lf: float | None = None
    ice_water_sf: float | None = None
    starter_lf: float | None = None
    felt_squares: float | None = None


@dataclass
class EstimateLineItem:
    source_file: str
    page_number: int
    item_number: str | None = None
    item_code: str | None = None
    category_code: str | None = None
    selector_code: str | None = None
    activity_code: str | None = None
    section_name: str | None = None
    coverage_name: str | None = None
    description: str = ""
    quantity: float | None = None
    unit: str | None = None
    unit_price: Decimal | None = None
    tax: Decimal | None = None
    replacement_cost: Decimal | None = None
    depreciation: Decimal | None = None
    actual_cash_value: Decimal | None = None
    overhead_and_profit: Decimal | None = None
    notes: list[str] = field(default_factory=list)
    confidence: float = 0.6

    @property
    def dedupe_key(self) -> tuple[str, str | None, float | None, str | None, str | None]:
        description = self.description.strip().lower()
        quantity = round(self.quantity, 4) if self.quantity is not None else None
        return (description, self.item_code, quantity, self.unit, self.section_name)


@dataclass
class ParsedEstimateDocument:
    source: SourceDocument
    metadata: EstimateMetadata
    totals: EstimateTotals
    roof: RoofMeasurements
    line_items: list[EstimateLineItem] = field(default_factory=list)
    warnings: list[ValidationMessage] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        _normalize_for_json(payload)
        return payload


@dataclass
class CanonicalEstimate:
    created_at: str
    merged_from_files: list[str]
    metadata: EstimateMetadata
    totals: EstimateTotals
    roof: RoofMeasurements
    line_items: list[EstimateLineItem] = field(default_factory=list)
    source_documents: list[SourceDocument] = field(default_factory=list)
    warnings: list[ValidationMessage] = field(default_factory=list)
    debug_notes: list[str] = field(default_factory=list)

    @classmethod
    def empty(cls) -> "CanonicalEstimate":
        return cls(
            created_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            merged_from_files=[],
            metadata=EstimateMetadata(),
            totals=EstimateTotals(),
            roof=RoofMeasurements(),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        _normalize_for_json(payload)
        return payload

    def preview_summary(self) -> dict[str, Any]:
        totals = self.totals
        return {
            "carrier": self.metadata.carrier or "Unknown",
            "insured": self.metadata.insured_name or "Unknown",
            "claim_number": self.metadata.claim_number or "Unknown",
            "property_address": self.metadata.property_address or "Unknown",
            "estimate_number": self.metadata.estimate_number or "Unknown",
            "line_item_count": len(self.line_items),
            "grand_total": format_money(
                totals.grand_total
                or totals.replacement_cost_value
                or totals.total_if_incurred
                or totals.line_item_total
                or ZERO
            ),
            "rcv": format_money(totals.replacement_cost_value or totals.grand_total or ZERO),
            "acv": format_money(totals.actual_cash_value or totals.gross_acv or totals.net_payable or ZERO),
            "net_payable": format_money(totals.net_payable or ZERO),
            "deductible": format_money(totals.deductible or ZERO),
            "scan_modes": ", ".join(sorted({source.scan_classification for source in self.source_documents})) or "native",
        }


def _normalize_for_json(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if isinstance(item, Decimal):
                value[key] = float(item)
            else:
                _normalize_for_json(item)
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            if isinstance(item, Decimal):
                value[index] = float(item)
            else:
                _normalize_for_json(item)
