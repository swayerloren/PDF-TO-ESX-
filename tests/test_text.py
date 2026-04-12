from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pdf_to_esx_agent.core.text import output_stem_from_paths, safe_filename


class TextUtilityTestCase(unittest.TestCase):
    def test_safe_filename_trims_invalid_characters_and_reserved_names(self) -> None:
        self.assertEqual(safe_filename("Report:*?<>|"), "Report")
        self.assertEqual(safe_filename("CON"), "CON_file")

    def test_output_stem_from_paths_is_deterministic_for_multiple_files(self) -> None:
        stem = output_stem_from_paths(
            [
                Path(r"C:\scopes\Claim Scope #1.pdf"),
                Path(r"C:\scopes\Claim Scope #2.pdf"),
            ]
        )
        self.assertEqual(stem, "Claim Scope 1_merged_2_files")
        reversed_stem = output_stem_from_paths(
            [
                Path(r"C:\scopes\Claim Scope #2.pdf"),
                Path(r"C:\scopes\Claim Scope #1.pdf"),
            ]
        )
        self.assertEqual(reversed_stem, stem)


if __name__ == "__main__":
    unittest.main()
