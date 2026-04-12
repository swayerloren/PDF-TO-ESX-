from __future__ import annotations

import logging
from pathlib import Path

from pdf_to_esx_agent.extract.line_items import LineItemExtractor
from pdf_to_esx_agent.extract.measurements import MeasurementsExtractor
from pdf_to_esx_agent.extract.metadata import MetadataExtractor
from pdf_to_esx_agent.extract.totals import TotalsExtractor
from pdf_to_esx_agent.models.estimate import ParsedEstimateDocument, SourceDocument, ValidationMessage
from pdf_to_esx_agent.parsing.document_loader import DocumentLoader


class EstimatePdfParser:
    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger("pdf_to_esx_agent").getChild("parser")
        self._loader = DocumentLoader(logger=self._logger.getChild("document_loader"))
        self._metadata = MetadataExtractor()
        self._line_items = LineItemExtractor()
        self._totals = TotalsExtractor()
        self._measurements = MeasurementsExtractor()

    def parse_path(self, path: Path) -> ParsedEstimateDocument:
        self._logger.info("[parse] Loading PDF: %s", path)
        document = self._loader.load_pdf_bytes(path.name, path.read_bytes())
        warnings: list[ValidationMessage] = []
        if document.errors:
            warnings.extend(ValidationMessage("warning", error, context=path.name) for error in document.errors)
        if document.routed_page_count:
            self._logger.info(
                "[parse] PDF type detected for %s: %s (routed=%s, ocr_used=%s)",
                path.name,
                document.scan_classification,
                document.routed_page_count,
                document.ocr_page_count,
            )
        if not document.has_readable_text:
            reason = document.extraction_failure_reason or "PDF did not yield readable text."
            warnings.append(ValidationMessage("error", reason, context=path.name))
        if document.scan_pipeline_status == "unavailable":
            warnings.append(
                ValidationMessage(
                    "warning",
                    "OCR dependencies were unavailable for pages that appeared scanned or text-poor.",
                    context=path.name,
                )
            )

        metadata = self._metadata.extract(document, file_name=path.name)
        line_items, line_item_warnings = self._line_items.extract(document, source_file=path.name)
        warnings.extend(line_item_warnings)
        totals, total_warnings = self._totals.extract(document, line_items)
        warnings.extend(total_warnings)
        roof = self._measurements.extract(document, line_items)

        source = SourceDocument(
            file_name=path.name,
            file_path=str(path),
            page_count=document.page_count,
            readable_page_count=document.readable_page_count,
            extracted_text_char_count=document.extracted_text_char_count,
            scan_classification=document.scan_classification,
            text_source=document.text_source,
            ocr_attempted=document.ocr_attempted,
            ocr_used=document.ocr_used,
            ocr_page_count=document.ocr_page_count,
            warnings=[warning.message for warning in warnings if warning.level != "error"],
        )

        self._logger.info(
            "[parse] Parsed %s: pages=%s, line_items=%s, scan=%s, ocr_used=%s",
            path.name,
            source.page_count,
            len(line_items),
            source.scan_classification,
            source.ocr_page_count,
        )
        self._logger.info(
            "[parse] Parsed totals for %s: rcv=%s, acv=%s, deductible=%s",
            path.name,
            totals.replacement_cost_value,
            totals.actual_cash_value or totals.gross_acv or totals.net_payable,
            totals.deductible,
        )
        return ParsedEstimateDocument(
            source=source,
            metadata=metadata,
            totals=totals,
            roof=roof,
            line_items=line_items,
            warnings=warnings,
        )
