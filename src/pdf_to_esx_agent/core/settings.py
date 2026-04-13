from __future__ import annotations

from dataclasses import dataclass
import ctypes
import os
from pathlib import Path
import sys


@dataclass(frozen=True)
class AppSettings:
    app_title: str
    app_slug: str
    repo_root: Path
    runtime_root: Path
    docs_dir: Path
    logs_dir: Path
    output_root: Path
    debug: bool
    frozen: bool

    @property
    def default_output_dir(self) -> Path:
        return self.output_root / "generated"


def load_settings() -> AppSettings:
    source_root = Path(__file__).resolve().parents[3]
    frozen = bool(getattr(sys, "frozen", False))
    repo_root = _bundle_root(source_root)
    runtime_root = _runtime_root(source_root, frozen)
    output_root = _output_root(runtime_root, source_root, frozen)
    debug_raw = os.getenv("PDF_TO_ESX_DEBUG", "").strip().lower()
    debug = debug_raw in {"1", "true", "yes", "on"}
    return AppSettings(
        app_title="PDF TO ESX AGENT",
        app_slug="PDF-TO-ESX-Agent",
        repo_root=repo_root,
        runtime_root=runtime_root,
        docs_dir=repo_root / "docs",
        logs_dir=runtime_root / "logs",
        output_root=output_root,
        debug=debug,
        frozen=frozen,
    )


def _bundle_root(source_root: Path) -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return source_root


def _runtime_root(source_root: Path, frozen: bool) -> Path:
    if not frozen:
        return source_root
    known_folder = _windows_known_folder_path(28)
    if known_folder:
        return known_folder / "PDF-TO-ESX-Agent"
    local_appdata = os.getenv("LOCALAPPDATA", "").strip()
    if local_appdata:
        return Path(local_appdata).expanduser() / "PDF-TO-ESX-Agent"
    return Path.home() / "AppData" / "Local" / "PDF-TO-ESX-Agent"


def _output_root(runtime_root: Path, source_root: Path, frozen: bool) -> Path:
    if not frozen:
        return source_root / "sample_output"
    known_folder = _windows_known_folder_path(5)
    if known_folder:
        return known_folder / "PDF TO ESX AGENT"
    user_profile = os.getenv("USERPROFILE", "").strip()
    if user_profile:
        return Path(user_profile) / "Documents" / "PDF TO ESX AGENT"
    return runtime_root / "output"


def _windows_known_folder_path(csidl: int) -> Path | None:
    if os.name != "nt":
        return None
    try:
        buffer = ctypes.create_unicode_buffer(260)
        result = ctypes.windll.shell32.SHGetFolderPathW(None, csidl, None, 0, buffer)
    except (AttributeError, OSError):
        return None
    if result != 0 or not buffer.value:
        return None
    return Path(buffer.value)
