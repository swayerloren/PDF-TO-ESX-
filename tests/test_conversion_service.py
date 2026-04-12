from __future__ import annotations

import contextlib
import io
import logging
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pdf_to_esx_agent.core.conversion_service import ConversionError, ConversionService
from pdf_to_esx_agent.core.settings import load_settings


class ConversionServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = load_settings()
        self.logger = logging.getLogger("test_conversion_service")
        self.logger.disabled = True
        logging.getLogger("pypdf").disabled = True
        self.service = ConversionService(settings=self.settings, logger=self.logger)

    def test_invalid_pdf_raises_conversion_error(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            invalid_pdf = Path(tmp_dir) / "broken.pdf"
            invalid_pdf.write_text("not a real pdf", encoding="utf-8")

            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(ConversionError):
                    self.service.convert([invalid_pdf], Path(tmp_dir))

    def test_missing_pdf_raises_conversion_error(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            missing_pdf = Path(tmp_dir) / "missing.pdf"

            with self.assertRaises(ConversionError):
                self.service.convert([missing_pdf], Path(tmp_dir))

    def test_non_pdf_input_raises_conversion_error(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            text_path = Path(tmp_dir) / "not_a_pdf.txt"
            text_path.write_text("plain text", encoding="utf-8")

            with self.assertRaises(ConversionError):
                self.service.convert([text_path], Path(tmp_dir))

    def test_output_path_that_is_a_file_raises_conversion_error(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            valid_pdf = Path(tmp_dir) / "broken.pdf"
            valid_pdf.write_text("not a real pdf", encoding="utf-8")
            file_output = Path(tmp_dir) / "output.txt"
            file_output.write_text("not a directory", encoding="utf-8")

            with self.assertRaises(ConversionError):
                self.service.convert([valid_pdf], file_output)


if __name__ == "__main__":
    unittest.main()
