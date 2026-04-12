from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Callable

from pdf_to_esx_agent.core.merge import EstimateMerger
from pdf_to_esx_agent.core.settings import AppSettings
from pdf_to_esx_agent.core.text import output_stem_from_paths
from pdf_to_esx_agent.export.esx_writer import ExportPaths, EsxWriter
from pdf_to_esx_agent.export.validator import ExportValidationError
from pdf_to_esx_agent.extract.estimate_parser import EstimatePdfParser
from pdf_to_esx_agent.models.estimate import CanonicalEstimate, ParsedEstimateDocument, ValidationMessage


ProgressCallback = Callable[["ProgressUpdate"], None]


@dataclass(frozen=True)
class ProgressUpdate:
    stage: str
    message: str
    current: int
    total: int

    @property
    def percent(self) -> int:
        if self.total <= 0:
            return 0
        return int((self.current / self.total) * 100)


@dataclass(frozen=True)
class ConversionResult:
    canonical_estimate: CanonicalEstimate
    parsed_documents: list[ParsedEstimateDocument]
    export_paths: ExportPaths
    validation_messages: list[ValidationMessage]


class ConversionError(RuntimeError):
    pass


class ConversionService:
    def __init__(self, settings: AppSettings, *, logger: logging.Logger | None = None) -> None:
        self._settings = settings
        self._logger = logger or logging.getLogger("pdf_to_esx_agent").getChild("conversion")
        self._parser = EstimatePdfParser(logger=self._logger.getChild("parser"))
        self._merger = EstimateMerger()
        self._writer = EsxWriter(logger=self._logger.getChild("export"))

    def convert(
        self,
        pdf_paths: list[Path],
        output_dir: Path | None = None,
        *,
        progress_callback: ProgressCallback | None = None,
    ) -> ConversionResult:
        normalized_paths = self._normalize_pdf_paths(pdf_paths)
        destination = self._normalize_output_dir(output_dir)

        parsed_documents: list[ParsedEstimateDocument] = []
        total_steps = len(normalized_paths) + 3
        self._emit(progress_callback, "validate", "Validating selected PDF files.", 1, total_steps)

        for index, path in enumerate(normalized_paths, start=1):
            self._emit(
                progress_callback,
                "parse",
                f"Extracting estimate data from {path.name}.",
                index + 1,
                total_steps,
            )
            parsed_document = self._parser.parse_path(path)
            self._raise_if_document_unusable(parsed_document)
            parsed_documents.append(parsed_document)

        self._emit(
            progress_callback,
            "merge",
            "Normalizing parsed data into the canonical estimate model.",
            total_steps - 1,
            total_steps,
        )
        canonical = self._merger.merge(parsed_documents)
        self._augment_canonical_validation(canonical)
        self._raise_if_canonical_unusable(canonical)

        stem = output_stem_from_paths(normalized_paths)
        self._emit(
            progress_callback,
            "export",
            "Generating ESX/XML export artifacts.",
            total_steps,
            total_steps,
        )
        try:
            export_paths = self._writer.write_package(canonical, destination, stem)
        except ExportValidationError as exc:
            self._logger.exception("[export] Package validation failed.")
            raise ConversionError(f"Generated ESX output failed structural validation: {exc}") from exc

        self._logger.info("[convert] Conversion complete. Output ESX: %s", export_paths.esx_path)
        return ConversionResult(
            canonical_estimate=canonical,
            parsed_documents=parsed_documents,
            export_paths=export_paths,
            validation_messages=canonical.warnings,
        )

    def _normalize_pdf_paths(self, pdf_paths: list[Path]) -> list[Path]:
        normalized: list[Path] = []
        seen: set[Path] = set()
        for raw_path in pdf_paths:
            path = Path(raw_path).expanduser().resolve()
            if not path.exists():
                raise ConversionError(f"Selected file does not exist: {path}")
            if path.suffix.lower() != ".pdf":
                raise ConversionError(f"Only PDF files are supported: {path.name}")
            if path in seen:
                self._logger.info("[validate] Ignoring duplicate PDF selection: %s", path)
                continue
            seen.add(path)
            normalized.append(path)
        if not normalized:
            raise ConversionError("Select at least one insurance estimate PDF.")
        return normalized

    def _normalize_output_dir(self, output_dir: Path | None) -> Path:
        raw_destination = output_dir or self._settings.default_output_dir
        destination = Path(raw_destination).expanduser().resolve()
        if destination.exists() and not destination.is_dir():
            raise ConversionError(f"Selected output path is not a folder: {destination}")
        try:
            destination.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise ConversionError(f"Could not create or access the output folder: {destination}") from exc
        self._logger.info("[validate] Using output folder: %s", destination)
        return destination

    def _raise_if_document_unusable(self, document: ParsedEstimateDocument) -> None:
        source = document.source
        issues: list[str] = []
        if source.page_count == 0:
            issues.append(f"{source.file_name}: the file could not be opened as a readable PDF.")
        elif source.readable_page_count == 0:
            if source.scan_classification in {"scanned", "mixed"} and not source.ocr_used:
                issues.append(
                    f"{source.file_name}: no readable text was extracted. The PDF appears scanned and OCR did not recover usable text."
                )
            else:
                issues.append(f"{source.file_name}: no readable text was extracted from the PDF.")

        has_totals = any(
            value is not None
            for value in (
                document.totals.replacement_cost_value,
                document.totals.line_item_total,
                document.totals.grand_total,
                document.totals.net_payable,
            )
        )
        if not document.line_items and not has_totals:
            issues.append(
                f"{source.file_name}: the parser did not find estimate line items or usable totals."
            )

        if issues:
            raise ConversionError("\n".join(issues))

    def _augment_canonical_validation(self, canonical: CanonicalEstimate) -> None:
        warnings = list(canonical.warnings)
        if not canonical.line_items:
            warnings.append(
                ValidationMessage("error", "No estimate line items were available for export.", context="line_items")
            )
        if canonical.totals.replacement_cost_value is None and canonical.totals.line_item_total is not None:
            canonical.totals.replacement_cost_value = canonical.totals.line_item_total
            warnings.append(
                ValidationMessage(
                    "warning",
                    "Replacement cost value was missing and was reconstructed from parsed line items.",
                    context="totals",
                )
            )
        if canonical.totals.grand_total is None and canonical.totals.replacement_cost_value is not None:
            canonical.totals.grand_total = canonical.totals.replacement_cost_value
        if canonical.metadata.claim_number is None:
            warnings.append(
                ValidationMessage("warning", "Claim number was not detected in the uploaded PDF set.", context="metadata")
            )
        if canonical.metadata.property_address is None:
            warnings.append(
                ValidationMessage("warning", "Property address was not detected in the uploaded PDF set.", context="metadata")
            )
        if any(source.scan_classification in {"scanned", "mixed"} for source in canonical.source_documents):
            if not any(source.ocr_used for source in canonical.source_documents):
                warnings.append(
                    ValidationMessage(
                        "warning",
                        "Some pages appeared scanned or degraded, but OCR did not contribute replacement text.",
                        context="ocr",
                    )
                )
        canonical.warnings = warnings

    def _raise_if_canonical_unusable(self, canonical: CanonicalEstimate) -> None:
        has_totals = any(
            value is not None
            for value in (
                canonical.totals.replacement_cost_value,
                canonical.totals.line_item_total,
                canonical.totals.grand_total,
                canonical.totals.net_payable,
            )
        )
        if not canonical.line_items and not has_totals:
            raise ConversionError(
                "The selected PDF files did not produce enough estimate data to build an ESX export."
            )

    def _emit(
        self,
        callback: ProgressCallback | None,
        stage: str,
        message: str,
        current: int,
        total: int,
    ) -> None:
        self._logger.info("[%s] %s", stage, message)
        if callback is not None:
            callback(ProgressUpdate(stage=stage, message=message, current=current, total=total))
