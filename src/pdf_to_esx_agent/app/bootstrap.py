from __future__ import annotations

import argparse
from pathlib import Path

from pdf_to_esx_agent.core.conversion_service import ConversionService
from pdf_to_esx_agent.core.logging import configure_logging
from pdf_to_esx_agent.core.settings import load_settings
from pdf_to_esx_agent.ui.main_window import MainWindow


def main(argv: list[str] | None = None) -> int:
    parser = _build_argument_parser()
    args = parser.parse_args(argv)
    settings = load_settings()
    app_logger = configure_logging(settings)
    app_logger.info("Starting %s", settings.app_title)

    conversion_service = ConversionService(
        settings=settings,
        logger=app_logger.getChild("conversion"),
    )
    if args.headless_convert:
        output_dir = Path(args.output_dir).expanduser() if args.output_dir else settings.default_output_dir
        result = conversion_service.convert([Path(path).expanduser() for path in args.headless_convert], output_dir)
        app_logger.info("Headless conversion complete. ESX: %s", result.export_paths.esx_path)
        return 0

    window = MainWindow(
        settings=settings,
        conversion_service=conversion_service,
        logger=app_logger.getChild("ui"),
    )
    window.run()
    return 0


def _build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "--headless-convert",
        nargs="+",
        metavar="PDF",
        help="Run a conversion without opening the GUI. Intended for validation and release testing.",
    )
    parser.add_argument(
        "--output-dir",
        metavar="PATH",
        help="Output directory for --headless-convert mode.",
    )
    return parser
