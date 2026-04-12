from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
from typing import Iterable


MONEY_QUANTUM = Decimal("0.01")
ZERO = Decimal("0.00")
_MONEY_TOKEN_RE = re.compile(r"[\(<+\-]?[A-Z$]?\d[\d,.]*[.,]\d{2}[>\)]?", re.IGNORECASE)
_NUMBER_RE = re.compile(r"(?<![A-Za-z])[-+]?\d[\d,]*(?:\.\d+)?")


def to_decimal(value: Decimal | float | int | str | None) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)
    if isinstance(value, (int, float)):
        return Decimal(str(value)).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)
    text = str(value).strip()
    if not text:
        return None
    negative = text.startswith("(") or text.startswith("<") or text.startswith("-")
    normalized = (
        text.replace("$", "")
        .replace("(", "")
        .replace(")", "")
        .replace("<", "")
        .replace(">", "")
        .replace("+", "")
        .replace(",", "")
        .strip()
    )
    try:
        parsed = Decimal(normalized)
    except (InvalidOperation, ValueError):
        return None
    if negative:
        parsed *= Decimal("-1")
    return parsed.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def money(value: Decimal | float | int | str | None) -> Decimal:
    return to_decimal(value) or ZERO


def quantize_number(value: Decimal | float | int | str | None, places: str = "0.01") -> Decimal | None:
    parsed = to_decimal(value)
    if parsed is None:
        return None
    return parsed.quantize(Decimal(places), rounding=ROUND_HALF_UP)


def sum_money(values: Iterable[Decimal | None]) -> Decimal:
    total = ZERO
    for value in values:
        if value is not None:
            total += money(value)
    return total.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def extract_money_tokens(text: str) -> list[str]:
    values: list[str] = []
    for token in _MONEY_TOKEN_RE.findall(text or ""):
        if to_decimal(token) is not None:
            values.append(token)
    return values


def extract_number_tokens(text: str) -> list[str]:
    values: list[str] = []
    for token in _NUMBER_RE.findall(text or ""):
        cleaned = token.replace(",", "").strip()
        if cleaned:
            values.append(cleaned)
    return values


def safe_float(value: Decimal | float | int | str | None) -> float | None:
    parsed = to_decimal(value)
    return float(parsed) if parsed is not None else None


def format_money(value: Decimal | None) -> str:
    if value is None:
        return ""
    return f"{value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP):,.2f}"

