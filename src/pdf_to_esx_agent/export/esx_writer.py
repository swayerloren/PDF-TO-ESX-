from __future__ import annotations

from dataclasses import dataclass, fields
import json
import logging
from pathlib import Path
import zipfile
from xml.etree import ElementTree as ET

from pdf_to_esx_agent import __version__
from pdf_to_esx_agent.core.numbers import MONEY_QUANTUM
from pdf_to_esx_agent.export.validator import ExportPackageValidator
from pdf_to_esx_agent.models.estimate import CanonicalEstimate, ValidationMessage


_ZIP_TIMESTAMP = (2024, 1, 1, 0, 0, 0)


@dataclass(frozen=True)
class ExportPaths:
    esx_path: Path
    xml_path: Path
    canonical_json_path: Path


class EsxWriter:
    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger("pdf_to_esx_agent").getChild("export")
        self._validator = ExportPackageValidator(logger=self._logger.getChild("validator"))

    def write_package(self, estimate: CanonicalEstimate, output_dir: Path, stem: str) -> ExportPaths:
        output_dir.mkdir(parents=True, exist_ok=True)
        self._logger.info("[export] Writing ESX artifacts with stem %s into %s", stem, output_dir)
        xml_tree = self._build_tree(estimate)
        xml_bytes = self._serialize_tree(xml_tree)
        self._validator.validate_xml_bytes(xml_bytes)

        canonical_json = json.dumps(estimate.to_dict(), indent=2, sort_keys=True)
        manifest = json.dumps(
            {
                "format": "pdf-to-esx-agent-package",
                "app": "PDF TO ESX AGENT",
                "version": __version__,
                "package_note": (
                    "Standards-based ESX-style package containing XACTDOC.XML and canonical estimate JSON. "
                    "It does not use the proprietary XACTDOC.ZIPXML packing used by some native ESX files."
                ),
                "source_files": estimate.merged_from_files,
            },
            indent=2,
            sort_keys=True,
        )

        xml_path = output_dir / f"{stem}.esx.xml"
        canonical_json_path = output_dir / f"{stem}.canonical.json"
        esx_path = output_dir / f"{stem}.esx"

        xml_path.write_bytes(xml_bytes)
        canonical_json_path.write_text(canonical_json, encoding="utf-8")

        with zipfile.ZipFile(esx_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            self._writestr(archive, "XACTDOC.XML", xml_bytes)
            self._writestr(archive, "canonical_estimate.json", canonical_json.encode("utf-8"))
            self._writestr(archive, "manifest.json", manifest.encode("utf-8"))

        self._validator.validate_package(esx_path, xml_bytes)

        self._logger.info("[export] ESX package generated at %s", esx_path)
        self._logger.info("[export] Companion XML generated at %s", xml_path)
        return ExportPaths(
            esx_path=esx_path,
            xml_path=xml_path,
            canonical_json_path=canonical_json_path,
        )

    def _build_tree(self, estimate: CanonicalEstimate) -> ET.Element:
        root = ET.Element(
            "XACTDOC",
            {
                "generatedBy": "PDF TO ESX AGENT",
                "schemaVersion": "0.1",
                "createdAt": estimate.created_at,
            },
        )

        self._append_project_info(root, estimate)
        self._append_params(root, estimate)
        self._append_adm(root)
        self._append_claim_info(root, estimate)
        self._append_contacts(root, estimate)
        self._append_group(root, estimate)
        self._append_embedded_price_list(root, estimate)
        self._append_totals(root, estimate)
        self._append_roof_measurements(root, estimate)
        self._append_source_documents(root, estimate)
        self._append_validation(root, estimate.warnings)
        self._append_audit_entries(root)
        return root

    def _append_project_info(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        metadata = estimate.metadata
        project = ET.SubElement(root, "PROJECT_INFO")
        _set_text(project, "PROJECT_NAME", metadata.estimate_name or "Insurance Estimate Export")
        _set_text(project, "ESTIMATE_NUMBER", metadata.estimate_number)
        _set_text(project, "ESTIMATE_DATE", metadata.estimate_date)
        _set_text(project, "PRICE_LIST_CODE", metadata.price_list_code)
        _set_text(project, "PRICE_LIST_REGION", metadata.price_list_region)
        _set_text(project, "PRICE_LIST_MONTH", metadata.price_list_month)
        _set_text(project, "PRICE_LIST_YEAR", metadata.price_list_year)
        _set_text(project, "MERGED_FROM_FILES", ", ".join(estimate.merged_from_files))

    def _append_params(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        params = ET.SubElement(root, "PARAMS")
        ET.SubElement(params, "PARAM", {"name": "export_format", "value": "xactdoc_xml"})
        ET.SubElement(params, "PARAM", {"name": "package_layout", "value": "zip_with_xml"})
        ET.SubElement(params, "PARAM", {"name": "source_document_count", "value": str(len(estimate.source_documents))})
        ET.SubElement(params, "PARAM", {"name": "line_item_count", "value": str(len(estimate.line_items))})

    def _append_adm(self, root: ET.Element) -> None:
        adm = ET.SubElement(root, "ADM")
        ET.SubElement(adm, "SYSTEM", {"name": "PDF TO ESX AGENT", "version": __version__})
        ET.SubElement(adm, "EXPORT_MODE", {"value": "local_desktop"})

    def _append_claim_info(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        metadata = estimate.metadata
        claim = ET.SubElement(root, "CLAIM_INFO")
        _set_text(claim, "CARRIER", metadata.carrier)
        _set_text(claim, "CLAIM_NUMBER", metadata.claim_number)
        _set_text(claim, "POLICY_NUMBER", metadata.policy_number)
        _set_text(claim, "DATE_OF_LOSS", metadata.date_of_loss)
        _set_text(claim, "DATE_INSPECTED", metadata.date_inspected)
        _set_text(claim, "PROPERTY_ADDRESS", metadata.property_address)
        _set_text(claim, "CITY", metadata.city)
        _set_text(claim, "STATE", metadata.state)
        _set_text(claim, "POSTAL_CODE", metadata.postal_code)

    def _append_contacts(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        metadata = estimate.metadata
        contacts = ET.SubElement(root, "CONTACTS")
        insured = ET.SubElement(contacts, "CONTACT", {"role": "insured"})
        _set_text(insured, "NAME", metadata.insured_name)
        _set_text(insured, "ADDRESS", metadata.property_address)

        estimator = ET.SubElement(contacts, "CONTACT", {"role": "estimator"})
        _set_text(estimator, "NAME", metadata.estimator_name)
        _set_text(estimator, "PHONE", metadata.estimator_phone)
        _set_text(estimator, "EMAIL", metadata.estimator_email)

    def _append_group(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        group = ET.SubElement(root, "GROUP")
        items = ET.SubElement(group, "ITEMS")
        for index, line_item in enumerate(estimate.line_items, start=1):
            item = ET.SubElement(
                items,
                "ITEM",
                {
                    "id": str(index),
                    "sourceFile": line_item.source_file,
                    "page": str(line_item.page_number),
                },
            )
            _set_text(item, "ITEM_NUMBER", line_item.item_number)
            _set_text(item, "SECTION", line_item.section_name)
            _set_text(item, "COVERAGE", line_item.coverage_name)
            _set_text(item, "DESCRIPTION", line_item.description)
            ET.SubElement(item, "SUMMARY_REF", {"ref": f"SI{index}"})
            for note in line_item.notes:
                _set_text(item, "NOTE", note)

    def _append_embedded_price_list(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        metadata = estimate.metadata
        embedded = ET.SubElement(root, "EMBEDDED_PL")
        ET.SubElement(
            embedded,
            "PRICE_LIST",
            {
                "code": _string(metadata.price_list_code),
                "region": _string(metadata.price_list_region),
                "month": _string(metadata.price_list_month),
                "year": _string(metadata.price_list_year),
            },
        )

        sumitems = ET.SubElement(embedded, "SUMITEMS")
        for index, line_item in enumerate(estimate.line_items, start=1):
            attributes = {
                "id": f"SI{index}",
                "seq": str(index),
                "cat": _string(line_item.category_code),
                "sel": _string(line_item.selector_code),
                "act": _string(line_item.activity_code or "+"),
                "code": _string(line_item.item_code),
                "desc": _string(line_item.description),
                "unit": _string(line_item.unit),
                "qty": _format_number(line_item.quantity),
                "price": _format_decimal(line_item.unit_price),
                "tax": _format_decimal(line_item.tax),
                "rcv": _format_decimal(line_item.replacement_cost),
                "dep": _format_decimal(line_item.depreciation),
                "acv": _format_decimal(line_item.actual_cash_value),
                "op": _format_decimal(line_item.overhead_and_profit),
                "section": _string(line_item.section_name),
                "coverage": _string(line_item.coverage_name),
                "confidence": f"{line_item.confidence:.2f}",
            }
            sumitem = ET.SubElement(sumitems, "SUMITEM", attributes)
            for note in line_item.notes:
                _set_text(sumitem, "NOTE", note)

    def _append_totals(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        totals = ET.SubElement(root, "TOTALS")
        for field_info in fields(type(estimate.totals)):
            value = getattr(estimate.totals, field_info.name)
            if value is None:
                continue
            _set_text(totals, field_info.name.upper(), _format_decimal(value))

    def _append_roof_measurements(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        roof = ET.SubElement(root, "ROOF_MEASUREMENTS")
        for field_info in fields(type(estimate.roof)):
            value = getattr(estimate.roof, field_info.name)
            if value is None:
                continue
            _set_text(roof, field_info.name.upper(), _format_number(value))

    def _append_source_documents(self, root: ET.Element, estimate: CanonicalEstimate) -> None:
        documents = ET.SubElement(root, "SOURCE_DOCUMENTS")
        for source in estimate.source_documents:
            attrs = {
                "fileName": source.file_name,
                "filePath": source.file_path,
                "pageCount": str(source.page_count),
                "readablePageCount": str(source.readable_page_count),
                "scanClassification": source.scan_classification,
                "textSource": source.text_source,
                "ocrAttempted": str(source.ocr_attempted).lower(),
                "ocrUsed": str(source.ocr_used).lower(),
                "ocrPageCount": str(source.ocr_page_count),
            }
            document = ET.SubElement(documents, "DOCUMENT", attrs)
            for warning in source.warnings:
                _set_text(document, "WARNING", warning)

    def _append_validation(self, root: ET.Element, warnings: list[ValidationMessage]) -> None:
        validation = ET.SubElement(root, "VALIDATION")
        for warning in warnings:
            attrs = {"level": warning.level}
            if warning.context:
                attrs["context"] = warning.context
            _set_text(validation, "MESSAGE", warning.message, attrs=attrs)

    def _append_audit_entries(self, root: ET.Element) -> None:
        audit = ET.SubElement(root, "AUDIT_ENTRIES")
        _set_text(audit, "AUDIT_ENTRY", "Converted from uploaded PDF estimate documents.")
        _set_text(audit, "AUDIT_ENTRY", "Exported as standards-based XACTDOC XML package.")

    def _serialize_tree(self, root: ET.Element) -> bytes:
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        return ET.tostring(root, encoding="utf-8", xml_declaration=True)

    def _writestr(self, archive: zipfile.ZipFile, name: str, payload: bytes) -> None:
        info = zipfile.ZipInfo(filename=name, date_time=_ZIP_TIMESTAMP)
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, payload)


def _set_text(parent: ET.Element, tag: str, value: object, *, attrs: dict[str, str] | None = None) -> None:
    if value is None:
        return
    text = _string(value)
    if not text:
        return
    element = ET.SubElement(parent, tag, attrs or {})
    element.text = text


def _format_decimal(value: object) -> str:
    if value is None:
        return ""
    return f"{value.quantize(MONEY_QUANTUM):.2f}"


def _format_number(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def _string(value: object) -> str:
    if value is None:
        return ""
    return str(value)
