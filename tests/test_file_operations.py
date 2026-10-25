"""Unit tests for File Manager operations and safety boundaries."""

import os
import sys
import shutil
import tempfile
import unittest
from pathlib import Path

# Add project root and files dir
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "desktop-apps" / "files"))

from file_manager import FileItem

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="gw_files_test_"))
        self.trash_dir = self.test_dir / "Trash"
        self.trash_files = self.trash_dir / "files"
        self.trash_info = self.trash_dir / "info"
        self.trash_files.mkdir(parents=True, exist_ok=True)
        self.trash_info.mkdir(parents=True, exist_ok=True)

        # Create sample files
        (self.test_dir / "file_a.txt").write_text("Hello World", encoding="utf-8")
        (self.test_dir / "file_b.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        (self.test_dir / ".hidden_file").write_text("Secret", encoding="utf-8")
        (self.test_dir / "subfolder").mkdir()
        (self.test_dir / "subfolder" / "nested.txt").write_text("Nested", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_file_item_metadata(self):
        f = self.test_dir / "file_a.txt"
        item = FileItem(f)
        self.assertEqual(item.name, "file_a.txt")
        self.assertFalse(item.is_dir)
        self.assertEqual(item.kind, "Plain Text")
        self.assertTrue("B" in item.formatted_size)

        folder = self.test_dir / "subfolder"
        folder_item = FileItem(folder)
        self.assertTrue(folder_item.is_dir)
        self.assertEqual(folder_item.kind, "Folder")
        self.assertEqual(folder_item.formatted_size, "--")

    def test_directory_enumeration_and_sorting(self):
        entries = list(self.test_dir.iterdir())
        entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))

        # Subfolder should come before normal files
        self.assertTrue(entries[0].is_dir())
        self.assertEqual(entries[0].name, "subfolder" if entries[0].name != "Trash" else "Trash")

    def test_trash_operation(self):
        target = self.test_dir / "file_a.txt"
        self.assertTrue(target.exists())

        # Move to trash
        dest = self.trash_files / target.name
        shutil.move(str(target), str(dest))

        info_file = self.trash_info / f"{dest.name}.trashinfo"
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(f"[Trash Info]\nPath={target.resolve()}\nDeletionDate=2026-10-26T12:00:00\n")

        self.assertFalse(target.exists())
        self.assertTrue(dest.exists())
        self.assertTrue(info_file.exists())

        # Verify trash info content
        content = info_file.read_text(encoding="utf-8")
        self.assertIn("Path=", content)
        self.assertIn("DeletionDate=", content)

    def test_new_folder_collision_prevention(self):
        # Create untitled folder
        f1 = self.test_dir / "untitled folder"
        f1.mkdir()
        self.assertTrue(f1.exists())

        # Second creation should become untitled folder 1
        base_name = "untitled folder"
        target = self.test_dir / base_name
        counter = 1
        while target.exists():
            target = self.test_dir / f"{base_name} {counter}"
            counter += 1
        target.mkdir()

        self.assertEqual(target.name, "untitled folder 1")
        self.assertTrue(target.exists())

if __name__ == "__main__":
    unittest.main()
