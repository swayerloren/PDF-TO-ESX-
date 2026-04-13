from __future__ import annotations

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pdf_to_esx_agent.core import settings as settings_module


class SettingsTestCase(unittest.TestCase):
    def test_load_settings_uses_repo_local_paths_in_source_mode(self) -> None:
        settings = settings_module.load_settings()

        self.assertFalse(settings.frozen)
        self.assertEqual(settings.runtime_root, settings.repo_root)
        self.assertEqual(settings.logs_dir, settings.repo_root / "logs")
        self.assertEqual(settings.output_root, settings.repo_root / "sample_output")
        self.assertEqual(settings.default_output_dir, settings.repo_root / "sample_output" / "generated")

    def test_load_settings_uses_user_writable_paths_in_frozen_mode(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            exe_dir = tmp_path / "dist" / "PDF-TO-ESX-Agent"
            exe_dir.mkdir(parents=True, exist_ok=True)
            local_appdata = tmp_path / "LocalAppData"
            user_profile = tmp_path / "UserProfile"
            local_appdata.mkdir(parents=True, exist_ok=True)
            user_profile.mkdir(parents=True, exist_ok=True)

            with (
                mock.patch.object(settings_module.sys, "frozen", True, create=True),
                mock.patch.object(settings_module.sys, "executable", str(exe_dir / "PDF-TO-ESX-Agent.exe")),
                mock.patch.object(settings_module, "_windows_known_folder_path", return_value=None),
                mock.patch.dict(
                    settings_module.os.environ,
                    {
                        "LOCALAPPDATA": str(local_appdata),
                        "USERPROFILE": str(user_profile),
                    },
                    clear=False,
                ),
            ):
                settings = settings_module.load_settings()

            self.assertTrue(settings.frozen)
            self.assertEqual(settings.repo_root, exe_dir)
            self.assertEqual(settings.runtime_root, local_appdata / "PDF-TO-ESX-Agent")
            self.assertEqual(settings.logs_dir, local_appdata / "PDF-TO-ESX-Agent" / "logs")
            self.assertEqual(settings.output_root, user_profile / "Documents" / "PDF TO ESX AGENT")
            self.assertEqual(settings.default_output_dir, user_profile / "Documents" / "PDF TO ESX AGENT" / "generated")

    def test_load_settings_prefers_known_windows_folders_in_frozen_mode(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            exe_dir = tmp_path / "dist" / "PDF-TO-ESX-Agent"
            exe_dir.mkdir(parents=True, exist_ok=True)
            known_local_appdata = tmp_path / "KnownLocalAppData"
            known_documents = tmp_path / "KnownDocuments"
            known_local_appdata.mkdir(parents=True, exist_ok=True)
            known_documents.mkdir(parents=True, exist_ok=True)

            with (
                mock.patch.object(settings_module.sys, "frozen", True, create=True),
                mock.patch.object(settings_module.sys, "executable", str(exe_dir / "PDF-TO-ESX-Agent.exe")),
                mock.patch.object(
                    settings_module,
                    "_windows_known_folder_path",
                    side_effect=[known_local_appdata, known_documents],
                ),
                mock.patch.dict(
                    settings_module.os.environ,
                    {
                        "LOCALAPPDATA": str(tmp_path / "EnvLocalAppData"),
                        "USERPROFILE": str(tmp_path / "EnvUserProfile"),
                    },
                    clear=False,
                ),
            ):
                settings = settings_module.load_settings()

            self.assertEqual(settings.runtime_root, known_local_appdata / "PDF-TO-ESX-Agent")
            self.assertEqual(settings.logs_dir, known_local_appdata / "PDF-TO-ESX-Agent" / "logs")
            self.assertEqual(settings.output_root, known_documents / "PDF TO ESX AGENT")
            self.assertEqual(settings.default_output_dir, known_documents / "PDF TO ESX AGENT" / "generated")


if __name__ == "__main__":
    unittest.main()
