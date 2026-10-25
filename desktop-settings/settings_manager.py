"""Glasswave Settings Manager.

Provides robust, schema-validated configuration management, atomic file updates,
automatic timestamped backups, and safe recovery from corruption.
"""

import os
import sys
import json
import time
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

class ValidationError(ValueError):
    """Raised when configuration values fail schema validation."""
    pass

DEFAULT_CONFIG: Dict[str, Any] = {
    "schema_version": "1.0.0",
    "appearance": {
        "theme": "dark",
        "accent_color": "blue",
        "wallpaper_mode": "default",
        "custom_wallpaper_path": ""
    },
    "dock": {
        "icon_size": 52,
        "magnification_factor": 1.35,
        "autohide": False,
        "position": "bottom",
        "pinned_apps": [
            "glasswave-files",
            "glasswave-terminal",
            "glasswave-settings",
            "glasswave-calculator",
            "glasswave-monitor",
            "glasswave-screenshot"
        ],
        "show_running_indicators": True
    },
    "topbar": {
        "show_title": True,
        "show_battery": True,
        "clock_format_24h": False,
        "compact_spacing": False
    },
    "window_decorations": {
        "traffic_lights_position": "left",
        "shadow_intensity": "medium"
    },
    "materials": {
        "blur_enabled": True,
        "blur_strength": 8,
        "translucency_percent": 78,
        "opaque_fallback": False
    },
    "motion": {
        "animation_speed": 1.0,
        "reduced_motion": False
    }
}

class SettingsManager:
    def __init__(self, config_path: Optional[Path] = None, schema_path: Optional[Path] = None):
        if config_path is None:
            config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "glasswave"
            self.config_path = config_dir / "glasswave.json"
        else:
            self.config_path = Path(config_path)

        self.config_dir = self.config_path.parent
        self.backup_dir = self.config_dir / "backups"

        if schema_path is None:
            self.schema_path = Path(__file__).resolve().parent / "schema.json"
        else:
            self.schema_path = Path(schema_path)

        self.schema = self._load_schema()
        self._data: Dict[str, Any] = {}
        self.load()

    def _load_schema(self) -> Dict[str, Any]:
        if self.schema_path.exists():
            try:
                with open(self.schema_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def get_defaults(self) -> Dict[str, Any]:
        return json.loads(json.dumps(DEFAULT_CONFIG))

    def load(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            self._data = self.get_defaults()
            self.save()
            return self._data

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    raise ValueError("Empty configuration file")
                data = json.loads(content)
                self.validate(data)
                self._data = data
        except Exception as e:
            # Create a backup of corrupt file and restore defaults
            try:
                self.config_dir.mkdir(parents=True, exist_ok=True)
                corrupt_backup = self.config_dir / f"glasswave.json.corrupt.{int(time.time())}"
                if self.config_path.exists():
                    shutil.copy2(self.config_path, corrupt_backup)
            except Exception:
                pass
            self._data = self.get_defaults()
            self.save()

        return self._data

    def validate(self, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise ValidationError("Configuration must be a JSON object")

        if data.get("schema_version") != "1.0.0":
            raise ValidationError(f"Unsupported schema_version: {data.get('schema_version')}")

        for section in ["appearance", "dock", "topbar", "window_decorations", "materials", "motion"]:
            if section not in data or not isinstance(data[section], dict):
                raise ValidationError(f"Missing or invalid section: {section}")

        app = data["appearance"]
        if app.get("theme") not in ["dark", "light"]:
            raise ValidationError(f"Invalid appearance.theme: {app.get('theme')}")
        if app.get("accent_color") not in ["blue", "purple", "pink", "orange", "green", "graphite"]:
            raise ValidationError(f"Invalid appearance.accent_color: {app.get('accent_color')}")
        if app.get("wallpaper_mode") not in ["default", "custom"]:
            raise ValidationError(f"Invalid appearance.wallpaper_mode: {app.get('wallpaper_mode')}")

        dock = data["dock"]
        if not isinstance(dock.get("icon_size"), int) or not (32 <= dock["icon_size"] <= 96):
            raise ValidationError(f"Invalid dock.icon_size: {dock.get('icon_size')}")
        if not isinstance(dock.get("magnification_factor"), (int, float)) or not (1.0 <= dock["magnification_factor"] <= 2.0):
            raise ValidationError(f"Invalid dock.magnification_factor: {dock.get('magnification_factor')}")
        if not isinstance(dock.get("autohide"), bool):
            raise ValidationError(f"Invalid dock.autohide: {dock.get('autohide')}")
        if dock.get("position") not in ["bottom", "left", "right"]:
            raise ValidationError(f"Invalid dock.position: {dock.get('position')}")
        if not isinstance(dock.get("pinned_apps"), list):
            raise ValidationError(f"Invalid dock.pinned_apps: must be list")

        topbar = data["topbar"]
        if not isinstance(topbar.get("show_title"), bool):
            raise ValidationError("topbar.show_title must be boolean")
        if not isinstance(topbar.get("show_battery"), bool):
            raise ValidationError("topbar.show_battery must be boolean")

        win = data["window_decorations"]
        if win.get("traffic_lights_position") not in ["left", "right"]:
            raise ValidationError(f"Invalid traffic_lights_position: {win.get('traffic_lights_position')}")
        if win.get("shadow_intensity") not in ["low", "medium", "high"]:
            raise ValidationError(f"Invalid shadow_intensity: {win.get('shadow_intensity')}")

        mat = data["materials"]
        if not isinstance(mat.get("blur_enabled"), bool):
            raise ValidationError("materials.blur_enabled must be boolean")
        if not isinstance(mat.get("blur_strength"), int) or not (1 <= mat["blur_strength"] <= 15):
            raise ValidationError("materials.blur_strength must be integer between 1 and 15")

        mot = data["motion"]
        if not isinstance(mot.get("reduced_motion"), bool):
            raise ValidationError("motion.reduced_motion must be boolean")

    def get(self, section: str, key: str, default: Any = None) -> Any:
        return self._data.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value: Any) -> None:
        if section not in self._data:
            self._data[section] = {}
        candidate = json.loads(json.dumps(self._data))
        candidate[section][key] = value
        self.validate(candidate)
        self._data = candidate
        self.save()

    def update_section(self, section: str, values: Dict[str, Any]) -> None:
        candidate = json.loads(json.dumps(self._data))
        if section not in candidate:
            candidate[section] = {}
        candidate[section].update(values)
        self.validate(candidate)
        self._data = candidate
        self.save()

    def save(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        # Atomic write
        temp_fd, temp_path = tempfile.mkstemp(dir=str(self.config_dir), prefix="cfg_", suffix=".tmp")
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.chmod(temp_path, 0o600)
            os.replace(temp_path, self.config_path)
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

    def backup(self) -> Path:
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"glasswave_backup_{timestamp}.json"
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
        os.chmod(backup_file, 0o600)
        self._rotate_backups(keep=10)
        return backup_file

    def _rotate_backups(self, keep: int = 10) -> None:
        if not self.backup_dir.exists():
            return
        backups = sorted(self.backup_dir.glob("glasswave_backup_*.json"), key=os.path.getmtime)
        while len(backups) > keep:
            oldest = backups.pop(0)
            try:
                oldest.unlink()
            except OSError:
                pass

    def export_config(self, dest_path: Path) -> Path:
        dest = Path(dest_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
        return dest

    def import_config(self, src_path: Path) -> None:
        src = Path(src_path)
        if not src.exists():
            raise FileNotFoundError(f"Source file {src} not found")
        with open(src, "r", encoding="utf-8") as f:
            new_data = json.load(f)
        self.validate(new_data)
        self.backup()
        self._data = new_data
        self.save()

    def restore_backup(self, backup_file: Path) -> None:
        self.import_config(backup_file)

    def reset_to_defaults(self) -> None:
        self.backup()
        self._data = self.get_defaults()
        self.save()

    def sync_to_system(self) -> Dict[str, bool]:
        """Synchronize Glasswave preferences with native KDE Plasma 6 & KWin configs.

        Uses kwriteconfig6 and D-Bus reconfigure commands without modifying
        system files or destabilizing non-KDE sessions.
        """
        results = {
            "kdeglobals": False,
            "kwinrc": False,
            "kwin_reconfigured": False,
        }
        kwrite = shutil.which("kwriteconfig6") or shutil.which("kwriteconfig5")
        if not kwrite:
            return results

        try:
            # 1. Appearance / Color Scheme
            theme = self.get("appearance", "theme", "dark")
            color_scheme = "GlasswaveDark" if theme == "dark" else "GlasswaveLight"
            subprocess.run(
                [kwrite, "--file", "kdeglobals", "--group", "General", "--key", "ColorScheme", color_scheme],
                check=False,
                capture_output=True,
            )
            subprocess.run(
                [kwrite, "--file", "kdeglobals", "--group", "KDE", "--key", "colorScheme", color_scheme],
                check=False,
                capture_output=True,
            )
            results["kdeglobals"] = True

            # 2. Window Decorations & Button Placement (Traffic Lights on Left)
            subprocess.run(
                [kwrite, "--file", "kwinrc", "--group", "org.kde.kdecoration2", "--key", "ButtonsOnLeft", "XIA"],
                check=False,
                capture_output=True,
            )
            subprocess.run(
                [kwrite, "--file", "kwinrc", "--group", "org.kde.kdecoration2", "--key", "ButtonsOnRight", ""],
                check=False,
                capture_output=True,
            )
            subprocess.run(
                [kwrite, "--file", "kwinrc", "--group", "org.kde.kdecoration2", "--key", "theme", color_scheme],
                check=False,
                capture_output=True,
            )

            # 3. Motion & Animation Speed
            reduced_motion = self.get("motion", "reduced_motion", False)
            anim_speed = "0" if reduced_motion else str(int(self.get("motion", "animation_speed", 1.0)))
            subprocess.run(
                [kwrite, "--file", "kwinrc", "--group", "Compositing", "--key", "AnimationSpeed", anim_speed],
                check=False,
                capture_output=True,
            )

            # 4. Blur and Materials
            blur_on = "true" if self.get("materials", "blur_enabled", True) else "false"
            subprocess.run(
                [kwrite, "--file", "kwinrc", "--group", "Plugins", "--key", "blurEnabled", blur_on],
                check=False,
                capture_output=True,
            )
            results["kwinrc"] = True

            # 5. Notify KWin to reload configuration
            qdbus = shutil.which("qdbus-qt6") or shutil.which("qdbus")
            if qdbus:
                ret = subprocess.run(
                    [qdbus, "org.kde.KWin", "/KWin", "reconfigure"],
                    check=False,
                    capture_output=True,
                )
                if ret.returncode == 0:
                    results["kwin_reconfigured"] = True

        except Exception:
            pass

        return results

    def as_dict(self) -> Dict[str, Any]:
        return json.loads(json.dumps(self._data))
