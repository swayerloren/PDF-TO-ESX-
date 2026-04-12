from __future__ import annotations

from copy import deepcopy
from dataclasses import fields
from decimal import Decimal

from pdf_to_esx_agent.core.numbers import ZERO, money, sum_money
from pdf_to_esx_agent.models.estimate import (
    CanonicalEstimate,
    EstimateLineItem,
    EstimateMetadata,
    EstimateTotals,
    ParsedEstimateDocument,
    RoofMeasurements,
    ValidationMessage,
)


_ROOF_FIELDS = tuple(field_info.name for field_info in fields(RoofMeasurements))
_METADATA_FIELDS = tuple(field_info.name for field_info in fields(EstimateMetadata))
_METADATA_PRIORITY_FIELDS = {
    "claim_number",
    "policy_number",
    "property_address",
    "carrier",
    "insured_name",
    "estimate_number",
}


class EstimateMerger:
    def merge(self, documents: list[ParsedEstimateDocument]) -> CanonicalEstimate:
        if not documents:
            raise ValueError("At least one parsed estimate document is required.")

        ordered_documents = sorted(documents, key=lambda document: document.source.file_name.lower())
        warnings = list(self._collect_warnings(ordered_documents))
        debug_notes: list[str] = []

        metadata = self._merge_metadata(ordered_documents, warnings, debug_notes)
        line_items, duplicates_removed = self._merge_line_items(ordered_documents, debug_notes)
        totals = self._merge_totals(ordered_documents, line_items, warnings, debug_notes)
        roof = self._merge_roof(ordered_documents, warnings, debug_notes)

        if duplicates_removed:
            warnings.append(
                ValidationMessage(
                    "warning",
                    f"Merged line items removed {duplicates_removed} duplicate entries across uploaded PDFs.",
                )
            )
        if not line_items:
            warnings.append(ValidationMessage("warning", "The canonical estimate does not contain any line items."))

        canonical = CanonicalEstimate.empty()
        canonical.merged_from_files = [document.source.file_name for document in ordered_documents]
        canonical.metadata = metadata
        canonical.totals = totals
        canonical.roof = roof
        canonical.line_items = line_items
        canonical.source_documents = [deepcopy(document.source) for document in ordered_documents]
        canonical.warnings = sorted(
            warnings,
            key=lambda warning: (
                {"error": 0, "warning": 1, "info": 2}.get(warning.level, 9),
                (warning.context or "").lower(),
                warning.message.lower(),
            ),
        )
        canonical.debug_notes = debug_notes
        return canonical

    def _collect_warnings(self, documents: list[ParsedEstimateDocument]) -> list[ValidationMessage]:
        warnings: list[ValidationMessage] = []
        for document in documents:
            warnings.extend(deepcopy(document.warnings))
        return warnings

    def _merge_metadata(
        self,
        documents: list[ParsedEstimateDocument],
        warnings: list[ValidationMessage],
        debug_notes: list[str],
    ) -> EstimateMetadata:
        merged = EstimateMetadata()
        completeness_by_file = {
            document.source.file_name: _count_populated_fields(document.metadata) for document in documents
        }
        for field_name in _METADATA_FIELDS:
            candidates: list[tuple[object, ParsedEstimateDocument]] = []
            for document in documents:
                value = getattr(document.metadata, field_name)
                if _has_value(value):
                    candidates.append((value, document))
            if not candidates:
                continue

            chosen_value, chosen_document = max(
                candidates,
                key=lambda candidate: (
                    _metadata_value_score(candidate[0]),
                    completeness_by_file[candidate[1].source.file_name],
                    candidate[1].source.file_name.lower(),
                ),
            )
            setattr(merged, field_name, chosen_value)

            normalized_values = {_normalize_comparable_value(value) for value, _document in candidates}
            normalized_values.discard(None)
            if len(normalized_values) > 1 and field_name in _METADATA_PRIORITY_FIELDS:
                warnings.append(
                    ValidationMessage(
                        "warning",
                        f"Conflicting metadata detected for {field_name.replace('_', ' ')}; using value from {chosen_document.source.file_name}.",
                        context=field_name,
                    )
                )
            debug_notes.append(f"metadata.{field_name} <- {chosen_document.source.file_name}")
        return merged

    def _merge_line_items(
        self,
        documents: list[ParsedEstimateDocument],
        debug_notes: list[str],
    ) -> tuple[list[EstimateLineItem], int]:
        merged_items: dict[tuple[object, ...], EstimateLineItem] = {}
        duplicates_removed = 0

        all_items = [
            deepcopy(item)
            for document in documents
            for item in sorted(document.line_items, key=_line_item_sort_key)
        ]

        for item in all_items:
            dedupe_key = self._line_item_dedupe_key(item)
            existing = merged_items.get(dedupe_key)
            if existing is None:
                merged_items[dedupe_key] = item
                continue
            duplicates_removed += 1
            preferred = existing if _line_item_score(existing) >= _line_item_score(item) else item
            alternate = item if preferred is existing else existing
            for field_info in fields(EstimateLineItem):
                field_name = field_info.name
                preferred_value = getattr(preferred, field_name)
                alternate_value = getattr(alternate, field_name)
                if not _has_value(preferred_value) and _has_value(alternate_value):
                    setattr(preferred, field_name, alternate_value)
            merged_notes = list(preferred.notes)
            merged_notes.extend(note for note in alternate.notes if note not in merged_notes)
            duplicate_note = (
                f"Duplicate line item also found in {alternate.source_file} page {alternate.page_number}."
            )
            if duplicate_note not in merged_notes:
                merged_notes.append(duplicate_note)
            preferred.notes = merged_notes
            preferred.confidence = max(preferred.confidence, alternate.confidence)
            merged_items[dedupe_key] = preferred

        ordered_items = sorted(merged_items.values(), key=_line_item_sort_key)
        debug_notes.append(f"line_items.merged_count={len(ordered_items)}")
        return ordered_items, duplicates_removed

    def _line_item_dedupe_key(self, item: EstimateLineItem) -> tuple[object, ...]:
        return (
            item.dedupe_key,
            item.unit_price,
            item.replacement_cost,
            item.actual_cash_value,
            item.coverage_name,
        )

    def _merge_totals(
        self,
        documents: list[ParsedEstimateDocument],
        line_items: list[EstimateLineItem],
        warnings: list[ValidationMessage],
        debug_notes: list[str],
    ) -> EstimateTotals:
        best_document = max(
            documents,
            key=lambda document: (
                _count_populated_fields(document.totals),
                len(document.line_items),
                document.source.readable_page_count,
                document.source.file_name.lower(),
            ),
        )

        merged = deepcopy(best_document.totals)
        computed_line_total = sum_money(_line_item_rcv(item) for item in line_items)
        computed_tax_total = sum_money(item.tax for item in line_items)
        computed_depreciation = sum_money(item.depreciation for item in line_items)
        computed_actual_cash_value = sum_money(
            item.actual_cash_value if item.actual_cash_value is not None else _line_item_acv_fallback(item)
            for item in line_items
        )
        computed_overhead_and_profit = sum_money(item.overhead_and_profit for item in line_items)

        if computed_line_total > ZERO:
            merged.line_item_total = merged.line_item_total or computed_line_total
            merged.subtotal = merged.subtotal or merged.line_item_total or computed_line_total
            merged.replacement_cost_value = (
                merged.replacement_cost_value or merged.grand_total or computed_line_total
            )
        if computed_tax_total > ZERO and merged.tax_total is None:
            merged.tax_total = computed_tax_total
        if computed_depreciation > ZERO and merged.depreciation is None:
            merged.depreciation = computed_depreciation
        if computed_overhead_and_profit > ZERO and merged.overhead_and_profit is None:
            merged.overhead_and_profit = computed_overhead_and_profit
        if computed_actual_cash_value > ZERO and merged.actual_cash_value is None:
            merged.actual_cash_value = computed_actual_cash_value
        if merged.gross_acv is None:
            merged.gross_acv = merged.actual_cash_value
        if merged.grand_total is None:
            merged.grand_total = merged.replacement_cost_value or merged.line_item_total
        if merged.net_payable is None:
            net_payable = merged.actual_cash_value
            if net_payable is not None and merged.deductible is not None:
                net_payable -= merged.deductible
            if net_payable is not None and merged.prior_payments is not None:
                net_payable -= merged.prior_payments
            merged.net_payable = net_payable
        if merged.total_if_incurred is None and merged.net_payable is not None:
            total_if_incurred = merged.net_payable
            if merged.recoverable_depreciation is not None:
                total_if_incurred += merged.recoverable_depreciation
            merged.total_if_incurred = total_if_incurred
        if merged.recoverable_depreciation is None and merged.depreciation is not None:
            merged.recoverable_depreciation = merged.depreciation

        if (
            best_document.totals.replacement_cost_value is not None
            and computed_line_total > ZERO
            and abs(best_document.totals.replacement_cost_value - computed_line_total)
            > max(Decimal("250.00"), best_document.totals.replacement_cost_value * Decimal("0.05"))
        ):
            warnings.append(
                ValidationMessage(
                    "warning",
                    f"Parsed line-item replacement cost ({computed_line_total}) does not match extracted summary total "
                    f"from {best_document.source.file_name} ({best_document.totals.replacement_cost_value}).",
                    context="totals",
                )
            )

        debug_notes.append(f"totals.primary_source={best_document.source.file_name}")
        debug_notes.append(f"totals.computed_line_total={computed_line_total}")
        return merged

    def _merge_roof(
        self,
        documents: list[ParsedEstimateDocument],
        warnings: list[ValidationMessage],
        debug_notes: list[str],
    ) -> RoofMeasurements:
        roof = RoofMeasurements()
        for field_name in _ROOF_FIELDS:
            values = [
                float(getattr(document.roof, field_name))
                for document in documents
                if getattr(document.roof, field_name) is not None
            ]
            if not values:
                continue
            setattr(roof, field_name, round(max(values), 2))
            if len({round(value, 2) for value in values}) > 1:
                warnings.append(
                    ValidationMessage(
                        "warning",
                        f"Conflicting roof measurement values detected for {field_name.replace('_', ' ')}; using the largest value.",
                        context=field_name,
                    )
                )
        if roof.surface_area_sq_ft is None and roof.squares is not None:
            roof.surface_area_sq_ft = round(roof.squares * 100.0, 2)
        if roof.squares is None and roof.surface_area_sq_ft is not None:
            roof.squares = round(roof.surface_area_sq_ft / 100.0, 2)
        debug_notes.append(
            f"roof.measurement_fields={sum(1 for field_name in _ROOF_FIELDS if getattr(roof, field_name) is not None)}"
        )
        return roof


def _count_populated_fields(value_object: object) -> int:
    return sum(1 for field_info in fields(type(value_object)) if _has_value(getattr(value_object, field_info.name)))


def _metadata_value_score(value: object) -> tuple[int, int]:
    if isinstance(value, str):
        normalized = value.strip()
        return (1, len(normalized))
    if isinstance(value, int):
        return (1, value)
    if value is not None:
        return (1, 1)
    return (0, 0)


def _normalize_comparable_value(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized or None
    return value


def _line_item_score(item: EstimateLineItem) -> tuple[int, int, Decimal, float]:
    populated = sum(1 for field_info in fields(EstimateLineItem) if _has_value(getattr(item, field_info.name)))
    notes_count = len(item.notes)
    replacement_cost = item.replacement_cost or ZERO
    return (populated, notes_count, replacement_cost, item.confidence)


def _line_item_sort_key(item: EstimateLineItem) -> tuple[object, ...]:
    return (
        (item.section_name or "").lower(),
        (item.coverage_name or "").lower(),
        item.page_number,
        _sortable_item_number(item.item_number),
        (item.description or "").lower(),
        item.source_file.lower(),
    )


def _sortable_item_number(value: str | None) -> tuple[int, str]:
    if not value:
        return (10_000, "")
    digits = "".join(character for character in value if character.isdigit())
    if digits:
        try:
            return (int(digits), value.lower())
        except ValueError:
            pass
    return (10_000, value.lower())


def _line_item_rcv(item: EstimateLineItem) -> Decimal | None:
    if item.replacement_cost is not None:
        return item.replacement_cost
    if item.quantity is not None and item.unit_price is not None:
        return money(item.quantity) * item.unit_price
    return None


def _line_item_acv_fallback(item: EstimateLineItem) -> Decimal | None:
    if item.replacement_cost is None:
        return None
    if item.depreciation is None:
        return item.replacement_cost
    return item.replacement_cost - item.depreciation


def _has_value(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    return True
