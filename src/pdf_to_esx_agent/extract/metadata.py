from __future__ import annotations

from pathlib import Path
import re
from typing import Callable

from dateutil import parser as date_parser

from pdf_to_esx_agent.core.text import normalize_whitespace
from pdf_to_esx_agent.models.estimate import EstimateMetadata
from pdf_to_esx_agent.parsing.document_loader import LoadedDocument
from pdf_to_esx_agent.parsing.page_classifier import PageClassifier


CLAIM_NUMBER_RE = re.compile(r"Claim\s*Number\s*[:|]?\s*([A-Z0-9][A-Z0-9-]{4,})", re.IGNORECASE)
POLICY_NUMBER_RE = re.compile(r"Po(?:licy|llcy|llicy)\s*Number\s*[:|]?\s*([A-Z0-9][A-Z0-9-]{4,})", re.IGNORECASE)
ESTIMATE_NUMBER_RE = re.compile(r"Estimate\s*(?:Number|#)\s*[:|]?\s*([A-Z0-9._-]{3,})", re.IGNORECASE)
DATE_OF_LOSS_RE = re.compile(r"Date\s*of\s*Loss\s*[:|]?\s*([^\n]+)", re.IGNORECASE)
DATE_INSPECTED_RE = re.compile(r"Date\s*Inspected\s*[:|]?\s*([0-9/ :AMP-]+)", re.IGNORECASE)
ESTIMATE_DATE_RE = re.compile(r"Date(?:\s+Est\.)?\s*(?:Completed)?\s*[:|]?\s*([0-9/ :AMP-]+)", re.IGNORECASE)
INSURED_RE = re.compile(
    r"Insured\s*[:|]?\s*([A-Z0-9&',.\- ]+?)(?:\s{2,}|Home:|Business:|Cell:|Phone:|Property\s*:|Claim\s*Number\s*:|\|)",
    re.IGNORECASE,
)
PROPERTY_LINE_RE = re.compile(r"^\s*(?:Property(?:\s+Address)?|Location\s+of\s+Loss)\s*[:.]\s*(.+)", re.IGNORECASE)
STREET_LINE_RE = re.compile(r"^\d{2,6}\s+[A-Z0-9][A-Z0-9 .'\-#/]+$", re.IGNORECASE)
CITY_STATE_ZIP_RE = re.compile(r"^[A-Z .'\-]+,?\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?$", re.IGNORECASE)
CITY_ONLY_RE = re.compile(r"^[A-Z .'\-]{2,}$", re.IGNORECASE)
STATE_ZIP_RE = re.compile(r"^[A-Z]{2},?\s*\d{5}(?:-\d{4})?$", re.IGNORECASE)
PHONE_RE = re.compile(r"(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?:\s*(?:x|ext\.?)\s*\d+)?", re.IGNORECASE)
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
PRICE_LIST_RE = re.compile(r"\b([A-Z0-9]{4,}_[A-Z]{3}\d{2})\b")
DATE_TOKEN_RE = re.compile(
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}(?:\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)?",
    re.IGNORECASE,
)

LABEL_TERMS = (
    "claim number",
    "policy number",
    "date of loss",
    "date inspected",
    "property address",
    "property",
    "location of loss",
    "insured",
    "business",
    "home",
    "cell",
    "phone",
    "type of loss",
    "cause of loss",
    "loan number",
    "reported date",
    "estimate",
    "address",
    "city",
    "state/zip",
)

BAD_ESTIMATE_NAME_PHRASES = (
    "priced based on estimated market pricing",
    "included for your review",
    "reasonable cost necessary",
    "take advantage of our self-service options",
    "unit of measure",
    "reflects the reasonable cost",
    "estimate summary guide",
    "provided for reference only",
)

_CARRIERS = [
    "state farm",
    "allstate",
    "nationwide",
    "farmers",
    "liberty mutual",
    "travelers",
    "travellers",
    "usaa",
    "safeco",
    "ally claims",
    "chubb",
    "erie",
    "frontline",
    "auto owners",
    "american family",
    "progressive",
    "assurant",
]


class MetadataExtractor:
    def __init__(self) -> None:
        self._page_classifier = PageClassifier()

    def extract(self, document: LoadedDocument, *, file_name: str | None = None) -> EstimateMetadata:
        pages = self._page_classifier.actual_claim_pages(document)
        actual_text = "\n".join(page.text for page in pages)
        all_text = "\n".join(page.text for page in document.pages)
        lines = [line for page in pages for line in page.lines]

        claim_number = self._extract_claim_number(lines, actual_text)
        policy_number = self._extract_policy_number(lines, actual_text)
        property_address, city, state, postal_code = self._extract_property_address(lines)
        insured_name = self._extract_insured_name(lines, actual_text)
        price_list_code = _extract_group(PRICE_LIST_RE, actual_text)
        price_list_region = None
        price_list_month = None
        price_list_year = None
        if price_list_code and "_" in price_list_code:
            prefix, suffix = price_list_code.split("_", 1)
            price_list_region = prefix
            month = suffix[:3]
            year_suffix = suffix[3:]
            if month.isalpha():
                price_list_month = month
            if year_suffix.isdigit():
                price_list_year = 2000 + int(year_suffix)

        estimate_name = self._estimate_name(lines, actual_text, file_name=file_name)
        estimate_number = self._estimate_number(lines, actual_text)

        metadata = EstimateMetadata(
            estimate_name=estimate_name,
            estimate_number=estimate_number,
            estimate_date=_normalize_date(
                self._extract_labeled_value(lines, ("estimate date", "date completed"), validator=_looks_like_date_text)
                or _extract_group(ESTIMATE_DATE_RE, actual_text)
            ),
            carrier=self._detect_carrier(actual_text or all_text),
            insured_name=insured_name,
            property_address=property_address,
            city=city,
            state=state,
            postal_code=postal_code,
            claim_number=claim_number,
            policy_number=policy_number,
            date_of_loss=_normalize_date(
                self._extract_labeled_value(lines, ("date of loss",), validator=_looks_like_date_text)
                or _extract_group(DATE_OF_LOSS_RE, actual_text)
            ),
            date_inspected=_normalize_date(
                self._extract_labeled_value(lines, ("date inspected",), validator=_looks_like_date_text)
                or _extract_group(DATE_INSPECTED_RE, actual_text)
            ),
            estimator_name=self._extract_estimator_name(lines),
            estimator_phone=self._extract_estimator_phone(actual_text or all_text),
            estimator_email=self._extract_estimator_email(actual_text or all_text),
            price_list_code=price_list_code,
            price_list_region=price_list_region,
            price_list_month=price_list_month,
            price_list_year=price_list_year,
        )
        if not metadata.estimate_name and file_name:
            metadata.estimate_name = Path(file_name).stem
        return metadata

    def _detect_carrier(self, text: str) -> str | None:
        lowered = text.lower()
        for carrier in _CARRIERS:
            if carrier in lowered:
                return carrier.title()
        return None

    def _estimate_name(self, lines: list[str], text: str, *, file_name: str | None) -> str | None:
        candidates: list[str] = []
        labeled = self._extract_labeled_value(lines, ("estimate",), validator=_looks_like_estimate_title)
        if labeled:
            candidates.append(labeled)

        for line in lines[:40]:
            cleaned = normalize_whitespace(line)
            if _looks_like_estimate_title(cleaned):
                candidates.append(cleaned)
            if "estimate" in cleaned.lower() and len(cleaned.split()) <= 4:
                candidates.append(cleaned)

        for candidate in candidates:
            cleaned = _clean_estimate_name(candidate)
            if cleaned:
                return cleaned
        if file_name:
            return Path(file_name).stem
        return None

    def _estimate_number(self, lines: list[str], text: str) -> str | None:
        candidate = (
            self._extract_labeled_value(lines, ("estimate number", "estimate #"), validator=_looks_like_identifier)
            or _extract_group(ESTIMATE_NUMBER_RE, text)
        )
        if candidate and _looks_like_identifier(candidate):
            return candidate
        return None

    def _extract_claim_number(self, lines: list[str], text: str) -> str | None:
        candidate = self._extract_labeled_value(
            lines,
            ("claim number", "our claim number"),
            validator=_looks_like_claim_number,
        )
        if candidate:
            return candidate
        regex_value = _extract_group(CLAIM_NUMBER_RE, text)
        if regex_value and _looks_like_claim_number(regex_value):
            return regex_value
        return None

    def _extract_policy_number(self, lines: list[str], text: str) -> str | None:
        candidate = self._extract_labeled_value(lines, ("policy number",), validator=_looks_like_policy_number)
        if candidate:
            return candidate
        regex_value = _extract_group(POLICY_NUMBER_RE, text)
        if regex_value and _looks_like_policy_number(regex_value):
            return regex_value
        return None

    def _extract_insured_name(self, lines: list[str], text: str) -> str | None:
        for index, line in enumerate(lines):
            normalized = normalize_whitespace(line)
            insured_match = re.match(r"^\s*Insured\s*:\s*(.+)$", normalized, re.IGNORECASE)
            if insured_match:
                candidate = _truncate_label_tail(insured_match.group(1))
                if candidate and _looks_like_person_name(candidate):
                    return _clean_name(candidate)
                if index + 1 < len(lines):
                    next_line = normalize_whitespace(lines[index + 1]).strip(" ,")
                    if _looks_like_person_name(next_line):
                        return _clean_name(next_line)

            to_name_match = re.match(r"^\s*To:\s*Name\s*:\s*(.+)$", normalized, re.IGNORECASE)
            if to_name_match:
                candidate = _truncate_label_tail(to_name_match.group(1))
                if candidate and _looks_like_person_name(candidate):
                    return _clean_name(candidate)
        return _clean_name(_extract_group(INSURED_RE, text))

    def _extract_property_address(self, lines: list[str]) -> tuple[str | None, str | None, str | None, str | None]:
        for index, line in enumerate(lines):
            match = PROPERTY_LINE_RE.search(line)
            if not match:
                continue
            street = _normalize_street_address(match.group(1).split("|", 1)[0])
            if not street or _contains_label_term(street):
                continue
            city_state = ""
            if index + 1 < len(lines):
                city_state = _normalize_city_state_zip(lines[index + 1])
            if city_state and CITY_STATE_ZIP_RE.match(city_state):
                address = f"{street}, {city_state}".strip(" ,")
                city, state, postal_code = _split_city_state_zip(city_state)
                return address, city, state, postal_code
            if index + 2 < len(lines) and CITY_ONLY_RE.match(lines[index + 1]) and STATE_ZIP_RE.match(lines[index + 2]):
                city = normalize_whitespace(lines[index + 1])
                state_zip = normalize_whitespace(lines[index + 2])
                address = f"{street}, {city}, {state_zip}".replace(", ,", ",")
                city_name, state, postal_code = _split_city_state_zip(f"{city}, {state_zip}")
                return address, city_name, state, postal_code
            city, state, postal_code = _split_city_state_zip(street)
            return street, city, state, postal_code

        for index in range(len(lines) - 1):
            street = normalize_whitespace(lines[index]).strip(" ,")
            if not STREET_LINE_RE.match(street):
                continue
            street = _normalize_street_address(street)
            next_line = _normalize_city_state_zip(lines[index + 1])
            if CITY_STATE_ZIP_RE.match(next_line):
                address = f"{street}, {next_line}".strip(" ,")
                city, state, postal_code = _split_city_state_zip(next_line)
                return address, city, state, postal_code
            if index + 2 < len(lines):
                city_line = normalize_whitespace(lines[index + 1]).strip(" ,")
                state_zip_line = normalize_whitespace(lines[index + 2]).strip(" ,")
                if CITY_ONLY_RE.match(city_line) and STATE_ZIP_RE.match(state_zip_line):
                    address = f"{street}, {city_line}, {state_zip_line}"
                    city, state, postal_code = _split_city_state_zip(f"{city_line}, {state_zip_line}")
                    return address, city, state, postal_code
        return None, None, None, None

    def _extract_estimator_name(self, lines: list[str]) -> str | None:
        for index, line in enumerate(lines):
            lowered = line.lower()
            if "estimator:" in lowered or "adjuster:" in lowered or "claim rep" in lowered:
                value = _truncate_label_tail(line.split(":", 1)[-1])
                if value and _looks_like_person_name(value):
                    return value
            if any(role in lowered for role in ("claim specialist", "claims examiner", "adjuster", "estimator")):
                if index > 0:
                    previous = normalize_whitespace(lines[index - 1]).strip(" ,")
                    if _looks_like_person_name(previous):
                        return previous
        return None

    def _extract_estimator_phone(self, text: str) -> str | None:
        matches = PHONE_RE.findall(text or "")
        return matches[0] if matches else None

    def _extract_estimator_email(self, text: str) -> str | None:
        matches = EMAIL_RE.findall(text or "")
        return matches[0] if matches else None

    def _extract_labeled_value(
        self,
        lines: list[str],
        labels: tuple[str, ...],
        *,
        validator: Callable[[str | None], bool] | None = None,
        max_lookahead: int = 6,
    ) -> str | None:
        for index, line in enumerate(lines):
            normalized_line = normalize_whitespace(line)
            lowered_line = normalized_line.lower()
            for label in labels:
                label_pattern = re.compile(rf"\b{re.escape(label)}\b\s*[:|]?\s*(.*)", re.IGNORECASE)
                match = label_pattern.search(normalized_line)
                if not match:
                    continue
                inline_value = _truncate_label_tail(match.group(1))
                if inline_value and (validator is None or validator(inline_value)):
                    return inline_value
                for next_index in range(index + 1, min(index + 1 + max_lookahead, len(lines))):
                    candidate = normalize_whitespace(lines[next_index]).strip(" ,")
                    if not candidate:
                        continue
                    if candidate.lower() == lowered_line:
                        continue
                    if _contains_label_term(candidate):
                        continue
                    if validator is None or validator(candidate):
                        return candidate
        return None


def _extract_group(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text or "")
    if not match:
        return None
    return normalize_whitespace(match.group(1)).strip(" ,")


def _truncate_label_tail(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = normalize_whitespace(value).strip(" ,")
    if not cleaned:
        return None
    for term in LABEL_TERMS:
        cleaned = re.split(rf"\b{re.escape(term)}\b\s*[:|]?", cleaned, maxsplit=1, flags=re.IGNORECASE)[0]
    cleaned = normalize_whitespace(cleaned).strip(" ,")
    return cleaned or None


def _clean_name(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = normalize_whitespace(value).strip(" ,.-")
    if not cleaned:
        return None
    if any(token in cleaned.lower() for token in ("insurance company", "page", "estimate", "address", "city", "state/zip")):
        return None
    if re.search(r"\d{4,}", cleaned):
        return None
    return cleaned


def _clean_estimate_name(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = normalize_whitespace(value).strip(" ,.-")
    lowered = cleaned.lower()
    if not cleaned:
        return None
    if any(phrase in lowered for phrase in BAD_ESTIMATE_NAME_PHRASES):
        return None
    if len(cleaned) > 48:
        return None
    if re.search(r"\b(page|policy|claim number|unit of measure|reference only)\b", lowered):
        return None
    return cleaned


def _normalize_city_state_zip(value: str) -> str:
    cleaned = normalize_whitespace(value).strip(" ,")
    cleaned = re.sub(r",(?=[A-Z]{2}\b)", ", ", cleaned)
    cleaned = re.sub(r"([A-Z]{2})(\d{5}(?:-\d{4})?)$", r"\1 \2", cleaned)
    return cleaned.strip(" ,")


def _split_city_state_zip(value: str) -> tuple[str | None, str | None, str | None]:
    normalized = _normalize_city_state_zip(value)
    if not normalized:
        return None, None, None
    match = re.search(r"(?P<city>[A-Z .'\-]+),?\s*(?P<state>[A-Z]{2})\s*(?P<zip>\d{5}(?:-\d{4})?)?$", normalized, re.IGNORECASE)
    if not match:
        return None, None, None
    return (
        normalize_whitespace(match.group("city")),
        match.group("state").upper(),
        match.group("zip"),
    )


def _normalize_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        parsed = date_parser.parse(value, fuzzy=True)
    except Exception:
        token_match = DATE_TOKEN_RE.search(value)
        if token_match:
            try:
                parsed = date_parser.parse(token_match.group(0), fuzzy=True)
                return parsed.isoformat()
            except Exception:
                pass
        return normalize_whitespace(value)
    return parsed.isoformat()


def _looks_like_claim_number(value: str | None) -> bool:
    if not value:
        return False
    cleaned = normalize_whitespace(value).strip(" ,")
    lowered = cleaned.lower()
    if _contains_label_term(cleaned):
        return False
    if lowered in {"claim", "number", "policy"}:
        return False
    alnum = re.sub(r"[^a-z0-9]", "", lowered)
    if len(alnum) < 6:
        return False
    return bool(re.fullmatch(r"[A-Z0-9-]+", cleaned, flags=re.IGNORECASE))


def _looks_like_policy_number(value: str | None) -> bool:
    if not value:
        return False
    cleaned = normalize_whitespace(value).strip(" ,")
    if _contains_label_term(cleaned):
        return False
    alnum = re.sub(r"[^a-z0-9]", "", cleaned.lower())
    return len(alnum) >= 6 and bool(re.fullmatch(r"[A-Z0-9-]+", cleaned, flags=re.IGNORECASE))


def _looks_like_person_name(value: str | None) -> bool:
    if not value:
        return False
    cleaned = normalize_whitespace(value).strip(" ,")
    if _contains_label_term(cleaned):
        return False
    if re.search(r"\d", cleaned):
        return False
    words = re.findall(r"[A-Za-z&'.-]+", cleaned)
    return len(words) >= 2


def _looks_like_date_text(value: str | None) -> bool:
    if not value:
        return False
    if DATE_TOKEN_RE.search(value):
        return True
    try:
        date_parser.parse(value, fuzzy=True)
        return True
    except Exception:
        return False


def _looks_like_identifier(value: str | None) -> bool:
    if not value:
        return False
    cleaned = normalize_whitespace(value).strip(" ,")
    if _contains_label_term(cleaned):
        return False
    return len(cleaned) <= 32 and bool(re.fullmatch(r"[A-Z0-9._-]+", cleaned, flags=re.IGNORECASE))


def _looks_like_estimate_title(value: str | None) -> bool:
    cleaned = _clean_estimate_name(value)
    if not cleaned:
        return False
    if re.search(r"\d{3,}", cleaned):
        return False
    words = cleaned.split()
    return len(words) <= 6


def _contains_label_term(value: str | None) -> bool:
    if not value:
        return False
    lowered = normalize_whitespace(value).lower()
    return any(term in lowered for term in LABEL_TERMS)


def _normalize_street_address(value: str) -> str:
    cleaned = normalize_whitespace(value).strip(" ,")
    joined = re.match(r"^(?P<number>\d{2,6})(?P<body>[A-Z][A-Z0-9]+)$", cleaned)
    if joined:
        cleaned = f"{joined.group('number')} {joined.group('body')}"
    suffix_match = re.match(
        r"^(?P<number>\d{2,6}\s+)?(?P<stem>[A-Z0-9]+?)(?P<suffix>ROAD|RD|DRIVE|DR|TRAIL|TRL|STREET|ST|AVENUE|AVE|LANE|LN|COURT|CT|PLACE|PL|WAY)(?P<dir>NE|NW|SE|SW|N|S|E|W)?$",
        cleaned,
        re.IGNORECASE,
    )
    if suffix_match:
        number = suffix_match.group("number") or ""
        stem = suffix_match.group("stem")
        suffix = suffix_match.group("suffix")
        direction = suffix_match.group("dir") or ""
        cleaned = f"{number}{stem} {suffix} {direction}".strip()
    return normalize_whitespace(cleaned)
