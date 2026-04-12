from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class AppSettings:
    app_title: str
    repo_root: Path
    docs_dir: Path
    logs_dir: Path
    sample_output_dir: Path
    debug: bool

    @property
    def default_output_dir(self) -> Path:
        return self.sample_output_dir / "generated"


def load_settings() -> AppSettings:
    repo_root = Path(__file__).resolve().parents[3]
    debug_raw = os.getenv("PDF_TO_ESX_DEBUG", "").strip().lower()
    debug = debug_raw in {"1", "true", "yes", "on"}
    return AppSettings(
        app_title="PDF TO ESX AGENT",
        repo_root=repo_root,
        docs_dir=repo_root / "docs",
        logs_dir=repo_root / "logs",
        sample_output_dir=repo_root / "sample_output",
        debug=debug,
    )

