from __future__ import annotations

import logging
from pathlib import Path

from pdf_to_esx_agent.core.settings import AppSettings


def configure_logging(settings: AppSettings) -> logging.Logger:
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = settings.logs_dir / "pdf_to_esx_agent.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    file_handler = logging.FileHandler(Path(log_path), encoding="utf-8")
    file_handler.setFormatter(formatter)

    if not settings.frozen:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logger = logging.getLogger("pdf_to_esx_agent")
    logger.setLevel(root_logger.level)
    logger.debug("Logging initialized at %s", log_path)
    return logger
