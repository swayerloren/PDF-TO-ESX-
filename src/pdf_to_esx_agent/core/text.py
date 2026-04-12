from __future__ import annotations

from pathlib import Path
import re


_NON_FILENAME_RE = re.compile(r"[^A-Za-z0-9._ -]+")
_WHITESPACE_RE = re.compile(r"\s+")
_RESERVED_FILENAMES = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


def normalize_whitespace(value: str) -> str:
    normalized = value.replace("\x00", " ").replace("\u00a0", " ")
    normalized = normalized.replace("\u2010", "-").replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    normalized = normalized.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return _WHITESPACE_RE.sub(" ", normalized).strip()


def normalize_multiline_text(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    lines = [normalize_whitespace(line) for line in value.split("\n")]
    return "\n".join(line for line in lines if line)


def compact_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def safe_filename(value: str, *, fallback: str = "estimate", max_length: int = 96) -> str:
    normalized = normalize_whitespace(value or "")
    normalized = _NON_FILENAME_RE.sub("", normalized).strip(" .")
    if len(normalized) > max_length:
        normalized = normalized[:max_length].rstrip(" ._-")
    if normalized.lower() in _RESERVED_FILENAMES:
        normalized = f"{normalized}_file"
    return normalized or fallback


def output_stem_from_paths(paths: list[Path]) -> str:
    if not paths:
        return "estimate_export"
    ordered_paths = sorted(paths, key=lambda path: (path.name.lower(), str(path).lower()))
    if len(ordered_paths) == 1:
        return safe_filename(ordered_paths[0].stem, fallback="estimate_export")
    first = safe_filename(ordered_paths[0].stem, fallback="estimate")
    return f"{first}_merged_{len(paths)}_files"
