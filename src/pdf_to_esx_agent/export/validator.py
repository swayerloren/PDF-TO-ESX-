from __future__ import annotations

import json
import logging
from pathlib import Path
import zipfile
from xml.etree import ElementTree as ET


class ExportValidationError(RuntimeError):
    pass


class ExportPackageValidator:
    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger("pdf_to_esx_agent").getChild("export.validator")

    def validate_xml_bytes(self, payload: bytes) -> ET.Element:
        try:
            root = ET.fromstring(payload)
        except ET.ParseError as exc:
            raise ExportValidationError(f"Generated XML is not well-formed: {exc}") from exc

        if root.tag != "XACTDOC":
            raise ExportValidationError(f"Generated XML root must be XACTDOC, got {root.tag}.")

        required_sections = (
            "PROJECT_INFO",
            "CLAIM_INFO",
            "GROUP",
            "EMBEDDED_PL",
            "TOTALS",
            "SOURCE_DOCUMENTS",
            "VALIDATION",
        )
        missing = [section for section in required_sections if root.find(section) is None]
        if missing:
            raise ExportValidationError(
                f"Generated XML is missing required sections: {', '.join(missing)}."
            )

        summary_refs = {
            ref.attrib.get("ref")
            for ref in root.findall("./GROUP/ITEMS/ITEM/SUMMARY_REF")
            if ref.attrib.get("ref")
        }
        sumitem_ids = {
            node.attrib.get("id")
            for node in root.findall("./EMBEDDED_PL/SUMITEMS/SUMITEM")
            if node.attrib.get("id")
        }
        dangling_refs = sorted(ref for ref in summary_refs if ref not in sumitem_ids)
        if dangling_refs:
            raise ExportValidationError(
                f"Generated XML contains ITEM summary refs without matching SUMITEM ids: {', '.join(dangling_refs)}."
            )

        return root

    def validate_package(self, esx_path: Path, xml_payload: bytes) -> None:
        if not esx_path.exists():
            raise ExportValidationError(f"Expected ESX package was not written: {esx_path}")

        with zipfile.ZipFile(esx_path) as archive:
            names = set(archive.namelist())
            required_names = {"XACTDOC.XML", "canonical_estimate.json", "manifest.json"}
            missing = sorted(required_names - names)
            if missing:
                raise ExportValidationError(
                    f"Generated ESX package is missing required entries: {', '.join(missing)}."
                )

            package_xml = archive.read("XACTDOC.XML")
            self.validate_xml_bytes(package_xml)
            if package_xml != xml_payload:
                raise ExportValidationError("Packaged XACTDOC.XML does not match the standalone XML payload.")

            try:
                json.loads(archive.read("canonical_estimate.json").decode("utf-8"))
            except Exception as exc:
                raise ExportValidationError(f"canonical_estimate.json is not valid JSON: {exc}") from exc

            try:
                manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
            except Exception as exc:
                raise ExportValidationError(f"manifest.json is not valid JSON: {exc}") from exc

            if manifest.get("format") != "pdf-to-esx-agent-package":
                raise ExportValidationError("manifest.json does not declare the expected package format.")

        self._logger.info("[validate] Validated ESX package structure at %s", esx_path)
