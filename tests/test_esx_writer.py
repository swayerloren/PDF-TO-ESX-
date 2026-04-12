from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
import zipfile
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pdf_to_esx_agent.export.esx_writer import EsxWriter
from pdf_to_esx_agent.models.estimate import (
    CanonicalEstimate,
    EstimateLineItem,
    EstimateMetadata,
    EstimateTotals,
    RoofMeasurements,
    SourceDocument,
)


class EsxWriterTestCase(unittest.TestCase):
    def test_writer_creates_valid_package_and_xml(self) -> None:
        estimate = CanonicalEstimate.empty()
        estimate.merged_from_files = ["sample.pdf"]
        estimate.metadata = EstimateMetadata(
            estimate_name="Sample Estimate",
            estimate_number="EST-1001",
            carrier="State Farm",
            insured_name="Jane Doe",
            property_address="123 Main St, Duluth, GA 30096",
            claim_number="CLM-1",
        )
        estimate.totals = EstimateTotals(
            replacement_cost_value=Decimal("1500.00"),
            actual_cash_value=Decimal("1200.00"),
            deductible=Decimal("500.00"),
            net_payable=Decimal("700.00"),
            line_item_total=Decimal("1400.00"),
            grand_total=Decimal("1500.00"),
        )
        estimate.roof = RoofMeasurements(squares=12.5, surface_area_sq_ft=1250.0)
        estimate.line_items = [
            EstimateLineItem(
                source_file="sample.pdf",
                page_number=1,
                item_number="1",
                item_code="RFG300+",
                category_code="RFG",
                selector_code="300",
                activity_code="+",
                section_name="Roof",
                coverage_name="Dwelling",
                description="Laminated - comp. shingle rfg. - w/out felt",
                quantity=12.5,
                unit="SQ",
                unit_price=Decimal("112.00"),
                tax=Decimal("15.00"),
                replacement_cost=Decimal("1415.00"),
                depreciation=Decimal("215.00"),
                actual_cash_value=Decimal("1200.00"),
            )
        ]
        estimate.source_documents = [
            SourceDocument(
                file_name="sample.pdf",
                file_path="C:/sample.pdf",
                page_count=1,
                readable_page_count=1,
                extracted_text_char_count=1000,
            )
        ]

        with TemporaryDirectory() as tmp_dir:
            writer = EsxWriter()
            paths = writer.write_package(estimate, Path(tmp_dir), "sample_estimate")

            self.assertTrue(paths.esx_path.exists())
            self.assertTrue(paths.xml_path.exists())
            self.assertTrue(paths.canonical_json_path.exists())

            xml_root = ET.fromstring(paths.xml_path.read_bytes())
            self.assertEqual(xml_root.tag, "XACTDOC")

            with zipfile.ZipFile(paths.esx_path) as archive:
                self.assertEqual(
                    sorted(archive.namelist()),
                    ["XACTDOC.XML", "canonical_estimate.json", "manifest.json"],
                )


if __name__ == "__main__":
    unittest.main()
