"""Unit tests for Installer, Backup Manager, and Rollback."""

import os
import sys
import shutil
import tempfile
import subprocess
import unittest
from pathlib import Path

# Add project root and installer dir
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "desktop-installer"))

from backup_manager import KDEBackupManager

class TestInstallerAndRollback(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="gw_inst_test_"))
        self.config_dir = self.test_dir / "config"
        self.backup_dir = self.test_dir / "kde-backups"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy KDE configs
        (self.config_dir / "kwinrc").write_text("[org.kde.kdecoration2]\ntheme=Breeze\n", encoding="utf-8")
        (self.config_dir / "kdeglobals").write_text("[KDE]\ncolorScheme=BreezeDark\n", encoding="utf-8")

        self.mgr = KDEBackupManager(backup_root=self.backup_dir, config_root=self.config_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_backup_creation_and_checksum(self):
        snap = self.mgr.create_snapshot()
        self.assertTrue(snap.exists())
        self.assertTrue((snap / "backup_manifest.json").exists())
        self.assertTrue((snap / "kwinrc").exists())
        self.assertTrue((snap / "kdeglobals").exists())

        snapshots = self.mgr.list_snapshots()
        self.assertEqual(len(snapshots), 1)

    def test_restore_snapshot(self):
        self.mgr.create_snapshot()

        # Modify original configs
        (self.config_dir / "kwinrc").write_text("[org.kde.kdecoration2]\ntheme=GlasswaveDark\n", encoding="utf-8")
        self.assertIn("GlasswaveDark", (self.config_dir / "kwinrc").read_text(encoding="utf-8"))

        # Restore
        res = self.mgr.restore_latest()
        self.assertTrue(res)
        self.assertIn("Breeze", (self.config_dir / "kwinrc").read_text(encoding="utf-8"))

    def test_installer_dry_run(self):
        install_script = PROJECT_ROOT / "desktop-installer" / "install.sh"
        proc = subprocess.run([str(install_script), "--user", "--dry-run"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Installing Glasswave Desktop", proc.stdout)

if __name__ == "__main__":
    unittest.main()
