"""Unit tests validating all Desktop Assets, Metadata, Desktop Entries, and Schemas."""

import os
import json
import configparser
import xml.etree.ElementTree as ET
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class TestDesktopAssets(unittest.TestCase):
    def test_json_metadata_and_tokens(self):
        json_files = list(PROJECT_ROOT.glob("**/*.json"))
        self.assertGreater(len(json_files), 0)
        for jf in json_files:
            with self.subTest(file=jf.name):
                with open(jf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.assertIsInstance(data, (dict, list))

    def test_desktop_files_validity(self):
        desktop_files = [f for f in PROJECT_ROOT.glob("**/*.desktop") if f.is_file()]
        self.assertGreater(len(desktop_files), 0)
        for df in desktop_files:
            with self.subTest(file=df.name):
                parser = configparser.ConfigParser(interpolation=None)
                parser.read(df, encoding="utf-8")
                self.assertIn("Desktop Entry", parser.sections())
                entry = parser["Desktop Entry"]
                self.assertIn("Name", entry)
                self.assertIn("Exec", entry)
                self.assertIn("Icon", entry)
                self.assertEqual(entry.get("Type"), "Application")

    def test_color_schemes_syntax(self):
        color_files = list(PROJECT_ROOT.glob("desktop-theme/color-schemes/*.colors"))
        self.assertGreater(len(color_files), 0)
        for cf in color_files:
            with self.subTest(file=cf.name):
                parser = configparser.ConfigParser(interpolation=None)
                parser.read(cf, encoding="utf-8")
                self.assertIn("General", parser.sections())
                self.assertIn("ColorScheme", parser["General"])

    def test_icon_theme_index(self):
        index_theme = PROJECT_ROOT / "desktop-icons" / "Glasswave" / "index.theme"
        self.assertTrue(index_theme.exists())
        parser = configparser.ConfigParser(interpolation=None)
        parser.read(index_theme, encoding="utf-8")
        self.assertIn("Icon Theme", parser.sections())
        self.assertEqual(parser["Icon Theme"].get("Name"), "Glasswave")

    def test_svg_xml_well_formed(self):
        svg_files = list(PROJECT_ROOT.glob("**/*.svg"))
        self.assertGreater(len(svg_files), 0)
        for sf in svg_files:
            with self.subTest(file=sf.name):
                try:
                    tree = ET.parse(sf)
                    root = tree.getroot()
                    self.assertIn("svg", root.tag.lower())
                except ET.ParseError as e:
                    self.fail(f"Invalid SVG XML in {sf}: {e}")

    def test_rpm_spec_tags(self):
        spec_file = PROJECT_ROOT / "desktop-packaging" / "glasswave-desktop.spec"
        self.assertTrue(spec_file.exists())
        content = spec_file.read_text(encoding="utf-8")
        self.assertIn("Name:", content)
        self.assertIn("Version:", content)
        self.assertIn("Release:", content)
        self.assertIn("Summary:", content)
        self.assertIn("License:", content)
        self.assertIn("Requires:", content)
        self.assertIn("%prep", content)
        self.assertIn("%build", content)
        self.assertIn("%install", content)
        self.assertIn("%files", content)

if __name__ == "__main__":
    unittest.main()
