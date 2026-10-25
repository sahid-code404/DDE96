"""Automated ADR Coverage Audit.

Verifies that every non-generated implementation file across the project
is explicitly tracked and documented in at least one Architecture Decision Record (ADR).
"""

import os
import re
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_PREFIXES = [
    ".git",
    "build",
    "dist",
    "__pycache__",
]

EXCLUDED_EXTENSIONS = [
    ".pyc",
    ".tmp",
    ".swp"
]

class TestADRCoverage(unittest.TestCase):
    def setUp(self):
        self.adr_dir = PROJECT_ROOT / "docs" / "adr"
        self.documented_files = set()
        self._parse_adrs()

    def _parse_adrs(self):
        adr_files = list(self.adr_dir.glob("0*.md"))
        self.assertGreater(len(adr_files), 0, "No ADR files found in docs/adr/")

        # Pattern to match lines like: - `filename` or - filename
        item_pattern = re.compile(r"^\s*-\s+`?([a-zA-Z0-9_\-\./]+)`?")

        for adr in adr_files:
            content = adr.read_text(encoding="utf-8")
            in_affected_section = False
            for line in content.splitlines():
                if "## Exact List of Affected Files" in line or "## Exact List of Affected Files or Components" in line:
                    in_affected_section = True
                    continue
                elif in_affected_section and line.startswith("## "):
                    in_affected_section = False
                    continue

                if in_affected_section:
                    match = item_pattern.match(line.strip())
                    if match:
                        raw_path = match.group(1).strip()
                        self.documented_files.add(raw_path)

    def test_all_implementation_files_have_adr_coverage(self):
        undocumented = []
        total_files = 0

        for path in PROJECT_ROOT.glob("**/*"):
            if not path.is_file():
                continue

            rel_path = path.relative_to(PROJECT_ROOT).as_posix()

            # Skip excluded paths & extensions
            if any(rel_path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
                continue
            if any(rel_path.endswith(ext) for ext in EXCLUDED_EXTENSIONS):
                continue
            if "backups" in rel_path or "rpmbuild" in rel_path:
                continue

            # Skip ADR index itself
            if rel_path == "docs/adr/README.md":
                continue

            total_files += 1

            # Check if this exact file is in documented_files
            if rel_path not in self.documented_files:
                undocumented.append(rel_path)

        if undocumented:
            msg = (
                f"Found {len(undocumented)} undocumented implementation file(s) missing from ADRs:\n"
                + "\n".join(f"  - {f}" for f in sorted(undocumented))
                + f"\n\nTotal documented files in ADRs: {len(self.documented_files)}"
            )
            self.fail(msg)

        self.assertGreater(total_files, 20)

if __name__ == "__main__":
    unittest.main()
