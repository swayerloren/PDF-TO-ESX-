from __future__ import annotations

from decimal import Decimal
import re

from pdf_to_esx_agent.core.numbers import money
from pdf_to_esx_agent.core.text import normalize_whitespace
from pdf_to_esx_agent.models.estimate import EstimateLineItem, ValidationMessage
from pdf_to_esx_agent.parsing.document_loader import LoadedDocument
from pdf_to_esx_agent.parsing.page_classifier import PageClassifier


ITEM_START_RE = re.compile(r"^[+*]?\s*(?P<token>[0-9Il|\s]{1,5}[a-z]?)[\.,](?:\s+(?=\S)|(?=[A-Za-z]))")
QTY_UNIT_RE = re.compile(
    r"(?<![A-Za-z])(?P<qty>\d[\d,./]*)\s*(?P<unit>SQ|SF|LF|EA|HR|SY|CY|CF|RM|DA|DAY|MO|WK|RL|TN|TB|BX)\b",
    re.IGNORECASE,
)
SECTION_NOISE_RE = re.compile(
    r"^(avg\.?|cond\.?|deprec\.?|dep%|age/life|pricing|source[- ]eagleview|continued|notes?)$",
    re.IGNORECASE,
)
LINE_RATE_RE = re.compile(
    r"@\s*\$?(?P<rate>\d+(?:\.\d+)?)\s*per\s*(?P<unit>LF|SF|SQ|EA|HR|SY|CY|CF|RM|DA|DAY|MO|WK)\b",
    re.IGNORECASE,
)

_CODE_RULES: tuple[tuple[tuple[str, ...], str, str], ...] = (
    (("tear off", "dispose of comp. shingles"), "RFG", "ARMV"),
    (("laminated", "comp. shingle"), "RFG", "300"),
    (("composition shingles",), "RFG", "300"),
    (("roofing felt",), "RFG", "FELT15"),
    (("starter",), "RFG", "ASTR"),
    (("drip edge",), "RFG", "DRIP"),
    (("ridge vent",), "RFG", "VENTR"),
    (("ridge cap",), "RFG", "RIDGC"),
    (("ice", "water"), "RFG", "IWS"),
    (("step flashing",), "RFG", "STEP"),
    (("pipe jack",), "RFG", "PFLASH"),
    (("flue cap",), "FPL", "FLCP>"),
    (("flashing",), "RFG", "FLASH"),
    (("gutter / downspout",), "SFG", "GUTRS"),
    (("gutter",), "SFG", "GUTRS"),
    (("splash guard",), "SFG", "GSG"),
    (("dumpster",), "DMO", "FEE"),
    (("landfill",), "DMO", "FEE"),
    (("overhead", "profit"), "OHP", "PROFIT"),
    (("permit",), "FEE", "PERMIT"),
)


class LineItemExtractor:
    def __init__(self) -> None:
        self._page_classifier = PageClassifier()

    def extract(self, document: LoadedDocument, *, source_file: str) -> tuple[list[EstimateLineItem], list[ValidationMessage]]:
        line_items: list[EstimateLineItem] = []
        warnings: list[ValidationMessage] = []
        for page in self._page_classifier.line_item_pages(document):
            line_items.extend(self._parse_page(source_file=source_file, page_number=page.page_number, lines=page.lines))
        if not line_items:
            warnings.append(ValidationMessage("warning", "No line items were parsed from the estimate detail pages."))
        return line_items, warnings

    def _parse_page(self, *, source_file: str, page_number: int, lines: list[str]) -> list[EstimateLineItem]:
        buffers: list[tuple[list[str], str | None]] = []
        current: list[str] = []
        current_section: str | None = None

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            section_header = _extract_section_header(stripped)
            if section_header is not None:
                current_section = section_header
                continue
            if _match_item_start(stripped):
                if current:
                    buffers.append((current, current_section))
                current = [stripped]
                continue
            if current:
                current.append(stripped)
        if current:
            buffers.append((current, current_section))

        parsed: list[EstimateLineItem] = []
        for buffer, section_name in buffers:
            item = self._parse_buffer(
                source_file=source_file,
                page_number=page_number,
                lines=buffer,
                section_name=section_name,
            )
            if item is not None:
                parsed.append(item)
        return parsed

    def _parse_buffer(
        self,
        *,
        source_file: str,
        page_number: int,
        lines: list[str],
        section_name: str | None,
    ) -> EstimateLineItem | None:
        first_line = lines[0]
        match = _match_item_start(first_line)
        if not match:
            return None
        item_number = _normalize_item_number_token(match.group("token"))
        numeric_index = self._find_numeric_line_index(lines)
        if numeric_index is None:
            return None

        notes = " ".join(lines[numeric_index + 1 :]).strip()
        numeric_line = lines[numeric_index]
        description = self._extract_description(lines[:numeric_index] if numeric_index > 0 else [first_line])
        numeric_fragment = _strip_item_prefix(numeric_line if numeric_index > 0 else first_line)
        quantity_match = QTY_UNIT_RE.search(numeric_fragment)
        if quantity_match is None:
            return None

        quantity_text = quantity_match.group("qty")
        unit = quantity_match.group("unit").upper()
        quantity = _parse_quantity(quantity_text)
        financial_fragment = numeric_fragment[quantity_match.end() :].strip()
        money_matches = list(re.finditer(r"[\(<+\-]?[A-Z$]?\d[\d,.]*[.,]\d{2}[>\)]?", financial_fragment, re.IGNORECASE))
        money_tokens = [match.group(0) for match in money_matches]
        percent_flags = [
            financial_fragment[match.end() : match.end() + 2].strip().startswith("%")
            for match in money_matches
        ]
        unit_price, tax, rcv, depreciation, acv = _parse_financial_columns(money_tokens, percent_flags, quantity)
        if rcv is None and acv is None:
            inferred_total = _infer_total_from_notes(notes, quantity, unit)
            rcv = inferred_total
            acv = inferred_total
            depreciation = Decimal("0.00")

        description = normalize_whitespace(description)
        category_code, selector_code, activity_code = _infer_codes(description, notes)
        item_code = f"{category_code}{selector_code}{activity_code}" if category_code and selector_code and activity_code else None
        coverage_name = "Other Structures" if "other structure" in f"{description} {notes}".lower() else "Dwelling"
        overhead_and_profit = rcv if "overhead" in description.lower() and "profit" in description.lower() else None
        confidence = 0.9 if item_code else 0.65

        return EstimateLineItem(
            source_file=source_file,
            page_number=page_number,
            item_number=item_number,
            item_code=item_code,
            category_code=category_code,
            selector_code=selector_code,
            activity_code=activity_code,
            section_name=section_name,
            coverage_name=coverage_name,
            description=description,
            quantity=quantity,
            unit=unit,
            unit_price=unit_price,
            tax=tax,
            replacement_cost=rcv,
            depreciation=depreciation,
            actual_cash_value=acv,
            overhead_and_profit=overhead_and_profit,
            notes=[notes] if notes else [],
            confidence=confidence,
        )

    def _find_numeric_line_index(self, lines: list[str]) -> int | None:
        for index, line in enumerate(lines):
            stripped = _strip_item_prefix(line)
            if QTY_UNIT_RE.search(stripped):
                return index
        return None

    def _extract_description(self, lines: list[str]) -> str:
        description_parts: list[str] = []
        for line in lines:
            stripped = _strip_item_prefix(line)
            if not stripped:
                continue
            if _looks_numeric_heavy(stripped):
                break
            description_parts.append(stripped)
        return " ".join(description_parts).strip()


def _strip_item_prefix(value: str) -> str:
    return ITEM_START_RE.sub("", value, count=1).strip()


def _match_item_start(value: str) -> re.Match[str] | None:
    return ITEM_START_RE.match(value)


def _normalize_item_number_token(value: str) -> str:
    cleaned = re.sub(r"\s+", "", value or "")
    return cleaned.replace("|", "1").replace("I", "1").replace("l", "1")


def _parse_quantity(value: str) -> float | None:
    cleaned = value.replace(",", "").strip()
    if "/" in cleaned and not cleaned.startswith("http"):
        parts = cleaned.split("/", 1)
        try:
            return float(parts[0]) / float(parts[1])
        except Exception:
            return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _parse_financial_columns(
    money_tokens: list[str],
    percent_flags: list[bool],
    quantity: float | None,
) -> tuple[Decimal | None, Decimal | None, Decimal | None, Decimal | None, Decimal | None]:
    values = [money(token) for token in money_tokens]
    if not values:
        return None, None, None, None, None
    unit_price: Decimal | None = None
    tax: Decimal | None = None
    rcv: Decimal | None = None
    depreciation: Decimal | None = None
    acv: Decimal | None = None

    unit_price = values[0]
    expected_total = _expected_total(quantity, unit_price)
    non_percent_entries = [
        (index, value)
        for index, value in enumerate(values)
        if index == 0 or index >= len(percent_flags) or not percent_flags[index]
    ]
    rcv_index = _choose_rcv_index(non_percent_entries, expected_total)

    if rcv_index is not None:
        rcv = values[rcv_index]
        tax_candidates = [
            value
            for index, value in non_percent_entries
            if 0 < index < rcv_index and (expected_total is None or _relative_difference(expected_total, value) > 0.25)
        ]
        tax = tax_candidates[-1] if tax_candidates else None

        tail_values = [value for index, value in non_percent_entries if index > rcv_index]
        if len(tail_values) >= 2:
            depreciation, acv = tail_values[-2:]
        elif len(tail_values) == 1:
            if any(percent_flags[index] for index in range(rcv_index + 1, min(len(percent_flags), len(values)))):
                depreciation = tail_values[0]
                acv = rcv - depreciation
            else:
                acv = tail_values[0]
                depreciation = abs(rcv - acv)
        else:
            acv = rcv
            depreciation = money(0)
    elif len(values) == 2:
        unit_price, rcv = values
        acv = rcv
        depreciation = money(0)
    elif len(values) == 1:
        rcv = values[0]
        acv = rcv
        depreciation = money(0)

    if unit_price is None and quantity:
        unit_price = (rcv / Decimal(str(quantity))).quantize(Decimal("0.01")) if rcv is not None else None
    if quantity and unit_price is not None and rcv is not None:
        expected = float(unit_price) * float(quantity)
        if expected and abs(expected - float(rcv)) / max(expected, 1.0) > 0.35:
            unit_price = (rcv / Decimal(str(quantity))).quantize(Decimal("0.01"))
    if depreciation is not None:
        depreciation = abs(depreciation)
    if tax is not None:
        tax = abs(tax)
    return unit_price, tax, rcv, depreciation, acv


def _infer_total_from_notes(notes: str, quantity: float | None, unit: str | None) -> Decimal | None:
    rate_match = LINE_RATE_RE.search(notes or "")
    if rate_match and unit and rate_match.group("unit").upper() == unit.upper() and quantity is not None:
        return (Decimal(str(quantity)) * money(rate_match.group("rate"))).quantize(Decimal("0.01"))
    return None


def _expected_total(quantity: float | None, unit_price: Decimal | None) -> Decimal | None:
    if quantity is None or unit_price is None:
        return None
    return (Decimal(str(quantity)) * unit_price).quantize(Decimal("0.01"))


def _choose_rcv_index(entries: list[tuple[int, Decimal]], expected_total: Decimal | None) -> int | None:
    if not entries:
        return None
    if expected_total is not None:
        candidates = [
            (index, value, _relative_difference(expected_total, value))
            for index, value in entries[1:]
            if value >= entries[0][1]
        ]
        close_matches = [candidate for candidate in candidates if candidate[2] <= 0.20]
        if close_matches:
            close_matches.sort(key=lambda candidate: (candidate[2], candidate[0]))
            return close_matches[0][0]
    if len(entries) >= 3:
        return entries[2][0]
    if len(entries) >= 2:
        return entries[1][0]
    return None


def _relative_difference(expected: Decimal | None, actual: Decimal | None) -> float:
    if expected is None or actual is None:
        return 9999.0
    expected_float = float(expected)
    actual_float = float(actual)
    return abs(expected_float - actual_float) / max(abs(expected_float), 1.0)


def _looks_numeric_heavy(value: str) -> bool:
    letters = sum(1 for char in value if char.isalpha())
    digits = sum(1 for char in value if char.isdigit())
    return digits > letters and bool(re.search(r"[\d$(),.%]", value))


def _extract_section_header(value: str) -> str | None:
    normalized = value.strip()
    if not normalized or len(normalized) <= 1:
        return None
    if ":" in normalized:
        return None
    if SECTION_NOISE_RE.match(normalized):
        return None
    if ITEM_START_RE.match(normalized):
        return None
    if QTY_UNIT_RE.search(normalized):
        return None
    if normalized[:1].isdigit():
        return None
    if len(normalized) > 50:
        return None
    alpha_tokens = re.findall(r"[A-Za-z]+", normalized)
    if not alpha_tokens:
        return None
    return normalized if normalized == normalized.upper() or normalized.istitle() else None


def _infer_codes(description: str, notes: str) -> tuple[str | None, str | None, str]:
    lowered = f"{description} {notes}".lower()
    activity = "+"
    if "tear off" in lowered or "remove" in lowered or "haul" in lowered:
        activity = "-"
    if "detach & reset" in lowered or "detach and reset" in lowered:
        activity = "&"
    for keywords, category, selector in _CODE_RULES:
        if all(keyword in lowered for keyword in keywords):
            return category, selector, activity
    return None, None, activity
