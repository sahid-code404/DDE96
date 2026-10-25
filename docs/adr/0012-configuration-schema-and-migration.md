# ADR-0012: Central Configuration Schema, Backup, and Reset

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
Desktop customizations frequently break because configurations are scattered across disparate INI files, registries, and environment variables without schema validation.
A corruption in one file can cause desktop startup crashes.
Furthermore, users need the ability to:
1. Export and import their settings cleanly.
2. Automatically create backups before any migration or upgrade.
3. Reset settings to pristine Glasswave defaults.
4. Safely revert to their prior KDE settings without losing personal data.

## Scope and Requirements
1. Author a formal JSON schema (`desktop-settings/schema.json`) defining all valid settings, types, constraints, and default values.
2. Build `SettingsManager` (`desktop-settings/settings_manager.py`) providing:
   - Schema validation against all read/write operations.
   - Automatic fallback to documented defaults when values are missing or malformed.
   - Automated timestamped backups before applying migrations (`~/.config/glasswave/backups/`).
   - Configuration export and import (JSON format).
   - Atomic configuration writes (write-to-temp and atomic rename) to eliminate corruption during power loss.
3. Provide a unified CLI tool `glasswave-config` (`desktop-settings/cli.py`) for scripted administration.

## Current Behavior / Previous Implementation
No configuration schema existed. Standard KDE settings are stored across dozens of independent RC files (`kdeglobals`, `kwinrc`, `plasmarc`, etc.) without a unified schema or validation layer.

## Decision Made
1. Author `desktop-settings/schema.json` version 1.0 covering:
   - `appearance`: theme (dark/light), accent_color, wallpaper_mode, custom_wallpaper_path.
   - `dock`: icon_size, magnification_factor, autohide, position, pinned_apps, show_running_indicators.
   - `topbar`: spacing, show_title, show_battery, clock_format_24h.
   - `window_decorations`: traffic_lights_position, shadow_intensity.
   - `materials`: blur_enabled, blur_strength, opacity, opaque_fallback.
   - `motion`: animation_speed, reduced_motion.
2. Implement `SettingsManager` with atomic file persistence using `tempfile.NamedTemporaryFile` followed by `os.replace`.
3. Implement automated backup rotation (retaining up to 10 latest timestamped snapshots).

## Detailed Rationale
A centralized JSON schema guarantees deterministic behavior, easy portability, atomic updates, and testability across Python, QML, and shell scripts.

## Alternatives Evaluated
1. **Using GSettings / dconf exclusively:** dconf is GNOME-centric and binary-based, making direct inspection, Git versioning, and KDE synchronization difficult.
2. **KConfig XT / C++ KConfig only:** KConfig lacks built-in JSON schema validation and cannot be easily queried by lightweight cross-toolkit scripts.

## Architecture and Implementation Consequences
- All Glasswave components read and modify settings via `SettingsManager` or the `glasswave-config` CLI.
- Changes are mirrored to relevant KDE config files when necessary.

## Dependencies and Version Constraints
- Python 3.10+
- Standard library (`json`, `shutil`, `tempfile`, `pathlib`).

## Security, Performance, and Accessibility
- **Security:** Permissions on `~/.config/glasswave/glasswave.json` set to `0600` (read/write by owner only); secrets are never stored in settings.
- **Performance:** In-memory caching avoids repeated disk reads; atomic writes prevent corruption.
- **Accessibility:** Reduced motion flag is centrally managed and immediately propagated.

## Exact List of Affected Files
- `desktop-settings/__init__.py`
- `desktop-settings/schema.json`
- `desktop-settings/settings_manager.py`
- `desktop-settings/cli.py`
- `docs/adr/0012-configuration-schema-and-migration.md`

## Tests Created or Modified
- `tests/test_config.py` (comprehensive unit tests: schema validation, default generation, corrupt JSON recovery, atomic write verification, export/import, backup rotation, reset)

## Build and Validation Results
All schema and persistence unit tests passed with 100% success.

## Known Limitations and Unresolved Risks
Direct manual edits to `glasswave.json` with external text editors will be validated on the next application launch; malformed keys are repaired and reverted to safe defaults.

## Rollback or Recovery Procedure
Execute `glasswave-config restore <backup-file>` or `glasswave-config reset`.

## Related ADRs
- Related to ADR-0001, ADR-0002, ADR-0006, and ADR-0013.
