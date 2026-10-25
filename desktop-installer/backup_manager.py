#!/usr/bin/env python3
"""Glasswave KDE Configuration Backup & Rollback Manager.

Safely snapshots user KDE Plasma settings prior to installing Glasswave,
and provides atomic restoration during rollback or uninstallation.
"""

import sys
import os
import json
import time
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Optional

KDE_CONFIG_FILES = [
    "kwinrc",
    "kdeglobals",
    "plasma-org.kde.plasma.desktop-appletsrc",
    "plasmarc",
    "kcminputrc"
]

class KDEBackupManager:
    def __init__(self, backup_root: Optional[Path] = None, config_root: Optional[Path] = None):
        self.config_root = config_root or Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        self.backup_root = backup_root or (self.config_root / "glasswave" / "kde-backups")

    def create_snapshot(self) -> Path:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        snapshot_dir = self.backup_root / timestamp
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "timestamp": timestamp,
            "created_at": time.time(),
            "files": {}
        }

        for fname in KDE_CONFIG_FILES:
            src = self.config_root / fname
            if src.exists():
                dst = snapshot_dir / fname
                shutil.copy2(src, dst)
                with open(src, "rb") as f:
                    digest = hashlib.sha256(f.read()).hexdigest()
                manifest["files"][fname] = {
                    "source": str(src),
                    "checksum": digest
                }

        manifest_file = snapshot_dir / "backup_manifest.json"
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return snapshot_dir

    def list_snapshots(self) -> List[Path]:
        if not self.backup_root.exists():
            return []
        return sorted([d for d in self.backup_root.iterdir() if d.is_dir() and (d / "backup_manifest.json").exists()], key=os.path.getmtime)

    def restore_latest(self) -> bool:
        snapshots = self.list_snapshots()
        if not snapshots:
            return False

        latest = snapshots[-1]
        manifest_file = latest / "backup_manifest.json"
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        for fname, meta in manifest.get("files", {}).items():
            src = latest / fname
            dst = Path(meta["source"])
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: backup_manager.py <backup|restore|list>")
        return 1

    mgr = KDEBackupManager()
    cmd = sys.argv[1].lower()

    if cmd == "backup":
        snap = mgr.create_snapshot()
        print(f"Created KDE backup snapshot at: {snap}")
        return 0
    elif cmd == "restore":
        if mgr.restore_latest():
            print("Successfully restored latest KDE backup snapshot.")
            return 0
        else:
            print("No KDE backup snapshot found to restore.")
            return 1
    elif cmd == "list":
        for s in mgr.list_snapshots():
            print(s.name)
        return 0
    else:
        print(f"Unknown command: {cmd}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
