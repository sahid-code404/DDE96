"""Unit tests for Glasswave Configuration and SettingsManager."""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

# Add project root and desktop-settings
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "desktop-settings"))

from settings_manager import SettingsManager, ValidationError, DEFAULT_CONFIG

class TestSettingsManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="gw_cfg_test_"))
        self.config_path = self.test_dir / "glasswave.json"
        self.schema_path = PROJECT_ROOT / "desktop-settings" / "schema.json"
        self.mgr = SettingsManager(config_path=self.config_path, schema_path=self.schema_path)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_default_initialization(self):
        self.assertTrue(self.config_path.exists())
        self.assertEqual(self.mgr.get("appearance", "theme"), "dark")
        self.assertEqual(self.mgr.get("appearance", "accent_color"), "blue")
        self.assertEqual(self.mgr.get("dock", "icon_size"), 52)
        self.assertEqual(self.mgr.get("dock", "magnification_factor"), 1.35)
        self.assertFalse(self.mgr.get("dock", "autohide"))
        self.assertTrue(self.mgr.get("materials", "blur_enabled"))
        self.assertEqual(self.mgr.get("materials", "blur_strength"), 8)
        self.assertFalse(self.mgr.get("motion", "reduced_motion"))

    def test_set_and_get_valid(self):
        self.mgr.set("appearance", "theme", "light")
        self.assertEqual(self.mgr.get("appearance", "theme"), "light")

        self.mgr.set("dock", "icon_size", 64)
        self.assertEqual(self.mgr.get("dock", "icon_size"), 64)

        self.mgr.set("motion", "reduced_motion", True)
        self.assertTrue(self.mgr.get("motion", "reduced_motion"))

    def test_validation_rejects_invalid_values(self):
        with self.assertRaises(ValidationError):
            self.mgr.set("appearance", "theme", "solarized")

        with self.assertRaises(ValidationError):
            self.mgr.set("dock", "icon_size", 12) # below minimum 32

        with self.assertRaises(ValidationError):
            self.mgr.set("dock", "icon_size", 128) # above maximum 96

        with self.assertRaises(ValidationError):
            self.mgr.set("materials", "blur_strength", 99) # above max 15

        with self.assertRaises(ValidationError):
            self.mgr.set("motion", "reduced_motion", "not_a_bool")

    def test_atomic_file_permissions(self):
        # File should have 0600 permissions
        st = os.stat(self.config_path)
        mode = st.st_mode & 0o777
        self.assertEqual(mode, 0o600)

    def test_corrupt_file_recovery(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write("{ INVALID JSON DATA CORRUPT")

        # Reload should catch error, backup corrupt file, and restore defaults
        recovered_mgr = SettingsManager(config_path=self.config_path, schema_path=self.schema_path)
        self.assertEqual(recovered_mgr.get("appearance", "theme"), "dark")

        # Check that corrupt file was preserved
        corrupt_files = list(self.test_dir.glob("glasswave.json.corrupt.*"))
        self.assertTrue(len(corrupt_files) > 0)

    def test_backup_and_rotation(self):
        backup_files = []
        for i in range(12):
            bf = self.mgr.backup()
            backup_files.append(bf)

        # Rotation should keep max 10
        current_backups = list(self.mgr.backup_dir.glob("glasswave_backup_*.json"))
        self.assertLessEqual(len(current_backups), 10)

    def test_export_and_import(self):
        export_file = self.test_dir / "custom_export.json"
        self.mgr.set("appearance", "accent_color", "purple")
        self.mgr.export_config(export_file)
        self.assertTrue(export_file.exists())

        # Reset and import
        self.mgr.reset_to_defaults()
        self.assertEqual(self.mgr.get("appearance", "accent_color"), "blue")

        self.mgr.import_config(export_file)
        self.assertEqual(self.mgr.get("appearance", "accent_color"), "purple")

if __name__ == "__main__":
    unittest.main()
