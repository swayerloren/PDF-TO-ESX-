from __future__ import annotations

import re

from pdf_to_esx_agent.core.numbers import money
from pdf_to_esx_agent.core.text import compact_text
from pdf_to_esx_agent.models.estimate import EstimateLineItem, EstimateTotals, ValidationMessage
from pdf_to_esx_agent.parsing.document_loader import LoadedDocument
from pdf_to_esx_agent.parsing.page_classifier import PageClassifier


_ALIASES: dict[str, tuple[str, ...]] = {
    "replacement_cost_value": ("replacement cost value", "repair replacement cost", "replacement cost", "total loss"),
    "actual_cash_value": ("actual cash value", "acv total", "total acv settlement"),
    "deductible": ("less deductible", "deductible"),
    "depreciation": ("less depreciation", "depreciation"),
    "recoverable_depreciation": ("total recoverable depreciation", "recoverable depreciation", "replacement cost benefits"),
    "prior_payments": ("prior payment", "less prior payments", "previous payment"),
    "net_payable": (
        "net actual cash value payment",
        "net payment",
        "total payable",
        "total payment amount",
        "net claim remaining",
        "amount payable",
    ),
    "total_if_incurred": (
        "total amount of claim if incurred",
        "total paid when incurred",
        "maximum additional amount available if incurred",
        "net claim remaining if depreciation is recovered",
        "net claim if additional amounts are recovered",
        "net claim if depreciation is recovered",
    ),
    "tax_total": ("material sales tax", "sales tax", "tax total"),
    "line_item_total": ("line item total", "line item totals", "item total", "subtotal"),
    "overhead_and_profit": ("overhead and profit", "o&p"),
    "grand_total": ("grand total", "total estimate", "estimate total"),
}


class TotalsExtractor:
    def __init__(self) -> None:
        self._page_classifier = PageClassifier()

    def extract(self, document: LoadedDocument, line_items: list[EstimateLineItem]) -> tuple[EstimateTotals, list[ValidationMessage]]:
        totals = EstimateTotals()
        warnings: list[ValidationMessage] = []
        scores: dict[str, int] = {}

        for page in self._page_classifier.summary_pages(document):
            candidate_lines = list(page.ocr_lines) if page.ocr_used and page.ocr_lines else page.lines
            for raw_line in candidate_lines:
                line = raw_line.text if hasattr(raw_line, "text") else str(raw_line)
                self._assign_from_line(line, totals, scores)

        if totals.replacement_cost_value is None and line_items:
            totals.replacement_cost_value = sum((item.replacement_cost or money(0)) for item in line_items)
            warnings.append(ValidationMessage("warning", "Replacement cost total was computed from parsed line items."))
        if totals.line_item_total is None and line_items:
            totals.line_item_total = sum((item.replacement_cost or money(0)) for item in line_items)
        if totals.tax_total is None and line_items:
            computed_tax = sum((item.tax or money(0)) for item in line_items)
            if computed_tax:
                totals.tax_total = computed_tax
        if totals.depreciation is None and line_items:
            computed_dep = sum((item.depreciation or money(0)) for item in line_items)
            if computed_dep:
                totals.depreciation = computed_dep
        if totals.actual_cash_value is None and line_items:
            computed_acv = sum((item.actual_cash_value or money(0)) for item in line_items)
            if computed_acv:
                totals.actual_cash_value = computed_acv
        if totals.gross_acv is None:
            totals.gross_acv = totals.actual_cash_value
        if totals.grand_total is None:
            totals.grand_total = totals.replacement_cost_value or totals.line_item_total
        if totals.net_payable is None:
            net = totals.actual_cash_value
            if net is not None and totals.deductible is not None:
                net -= totals.deductible
            if net is not None and totals.prior_payments is not None:
                net -= totals.prior_payments
            totals.net_payable = net
        if totals.replacement_cost_value is None and not line_items:
            warnings.append(ValidationMessage("warning", "No summary totals or line items were available to build estimate totals."))
        return totals, warnings

    def _assign_from_line(self, line: str, totals: EstimateTotals, scores: dict[str, int]) -> None:
        normalized = line.strip()
        compact = compact_text(normalized)
        tokens = re.findall(r"[\(<+\-]?[A-Z$]?\d[\d,.]*[.,]\d{2}[>\)]?", normalized, re.IGNORECASE)
        if not tokens:
            return
        amount = money(tokens[-1])
        best_field_name: str | None = None
        best_score = -1
        for field_name, aliases in _ALIASES.items():
            for alias in aliases:
                alias_compact = compact_text(alias)
                if alias_compact not in compact:
                    continue
                score = len(alias_compact)
                if score > best_score:
                    best_field_name = field_name
                    best_score = score

        if best_field_name is None:
            return

        value = abs(amount) if best_field_name in {"deductible", "depreciation", "prior_payments"} else amount
        existing = getattr(totals, best_field_name)
        if scores.get(best_field_name, -1) > best_score:
            return
        if scores.get(best_field_name, -1) == best_score and existing is not None:
            if abs(value) <= abs(existing):
                return

        setattr(totals, best_field_name, value)
        if best_field_name == "actual_cash_value" and totals.gross_acv is None:
            totals.gross_acv = value
        scores[best_field_name] = best_score
