from __future__ import annotations

from pdf_to_esx_agent.core.conversion_service import ConversionService
from pdf_to_esx_agent.core.logging import configure_logging
from pdf_to_esx_agent.core.settings import load_settings
from pdf_to_esx_agent.ui.main_window import MainWindow


def main() -> int:
    settings = load_settings()
    settings.default_output_dir.mkdir(parents=True, exist_ok=True)
    app_logger = configure_logging(settings)
    app_logger.info("Starting %s", settings.app_title)

    conversion_service = ConversionService(
        settings=settings,
        logger=app_logger.getChild("conversion"),
    )
    window = MainWindow(
        settings=settings,
        conversion_service=conversion_service,
        logger=app_logger.getChild("ui"),
    )
    window.run()
    return 0
