# ADR-0017: KDE System Settings Synchronization, Module Resolution, and Asset Integration

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
To satisfy the Master Prompt requirements:
1. "Where the setting belongs to an existing KDE system settings module, integrate with or navigate to that module rather than maintaining a competing implementation."
2. "Never present a switch as operational until its underlying setting is actually read and changed successfully."
3. "The terminal must provide a premium appearance and reuse Konsole or a supported terminal component."
4. When desktop applications (`glasswave-calculator`, `glasswave-monitor`, `glasswave-settings`, `glasswave-config`) are installed into `~/.local/bin` or `/usr/bin`, their supporting Python modules (`calculator_engine.py`, `monitor_engine.py`, `settings_manager.py`, `schema.json`) must be cleanly discoverable outside the source directory.
5. In `desktop-apps/screenshot/screenshot.py`, a missing `import shutil` was identified that would cause a `NameError` during Spectacle capture detection.

## Scope and Requirements
1. Implement a system synchronization routine in `desktop-settings/settings_manager.py` that translates Glasswave preferences (theme, animation speed, reduced motion, blur) to KDE Plasma 6 and KWin via `kwriteconfig6` and `qdbus-qt6` / `plasma-apply-lookandfeel`.
2. Add quick-access launcher buttons in `desktop-control-center/control_center.py` to open native KDE System Settings modules (`kcmshell6 kcm_colors`, `kcmshell6 kcm_kscreen`, `kcmshell6 kcm_animations`, `systemsettings`).
3. Deploy `desktop-apps/terminal/Glasswave.colorscheme` to `${DATA_DIR}/konsole/` across CMake, `install.sh`, and `glasswave-desktop.spec`.
4. Deploy supporting Python library modules to `${DATA_DIR}/glasswave/lib` and update application import search paths so executables run seamlessly both in-tree and post-installation.
5. Fix the missing `shutil` import in `desktop-apps/screenshot/screenshot.py`.
6. Add unit tests for system sync and installed module resolution.

## Current Behavior / Previous Implementation
- Changing settings in `control_center.py` persisted to `~/.config/glasswave/glasswave.json` but did not propagate immediately to KDE Plasma configuration (`kdeglobals`, `kwinrc`).
- `Glasswave.colorscheme` existed in `desktop-apps/terminal/` but was not staged to `${DATA_DIR}/konsole/`.
- Applications assumed helper modules resided in relative parent folders.
- `screenshot.py` lacked `import shutil`.

## Decision Made
1. Add `sync_to_system(self)` to `SettingsManager`:
   - Sets `ColorScheme` in `kdeglobals` (`GlasswaveDark` / `GlasswaveLight`).
   - Sets `AnimationSpeed` in `kwinrc` (`0` for reduced motion, else mapped multiplier).
   - Sets `blurEnabled` in `kwinrc` `[Plugins]`.
   - Signals KWin via `qdbus-qt6 org.kde.KWin /KWin reconfigure` or `qdbus org.kde.KWin /KWin reconfigure`.
2. In `control_center.py`, invoke `self.settings.sync_to_system()` on setting changes, and provide standard Gtk Buttons in the "About & System" view connecting to `kcmshell6`.
3. Add `import shutil` to `desktop-apps/screenshot/screenshot.py`.
4. Update `install.sh`, `CMakeLists.txt`, and `glasswave-desktop.spec` to install `Glasswave.colorscheme` to `share/konsole/` and helper libraries to `share/glasswave/lib/`.
5. Update `desktop-apps/calculator/calculator_ui.py`, `desktop-apps/monitor/monitor_ui.py`, `desktop-control-center/control_center.py`, and `desktop-settings/cli.py` to search `share/glasswave/lib` in `sys.path`.

## Detailed Rationale
Using `kwriteconfig6` and standard D-Bus reconfigure signals is KDE's recommended non-intrusive method to update settings at runtime. It avoids modifying system files, respects user configuration boundaries, and updates live sessions without restarting KWin.

## Alternatives Evaluated
1. **Directly writing to kdeglobals using INI parser:** Bypasses KDE's caching daemon (`kconf_update`) and risks losing concurrent changes made by native KDE apps. `kwriteconfig6` is safer and atomic.
2. **Reimplementing display resolution and scaling controls in Glasswave:** Unnecessary duplication of mature display management; delegating to `kcmshell6 kcm_kscreen` adheres strictly to the Master Prompt directive.

## Architecture and Implementation Consequences
- Full two-way harmony with native KDE Plasma 6 Wayland sessions.
- Seamless execution whether running standalone or installed system-wide.

## Dependencies and Version Constraints
- `kwriteconfig6` and optional `qdbus-qt6` / `plasma-apply-lookandfeel` (graceful fallback if not in path).
- Python 3.10+.

## Security, Performance, and Accessibility
- **Security:** `kwriteconfig6` is executed with sanitized arguments without shell expansion.
- **Performance:** Synchronization occurs on value commit rather than intermediate drag frames.
- **Accessibility:** Reduced motion toggle immediately sets KWin animation multiplier to 0 for instant, non-jarring window transitions.

## Exact List of Affected Files or Components
- `docs/adr/0017-kde-system-settings-synchronization.md`
- `desktop-settings/settings_manager.py`
- `desktop-control-center/control_center.py`
- `desktop-apps/screenshot/screenshot.py`
- `desktop-apps/calculator/calculator_ui.py`
- `desktop-apps/monitor/monitor_ui.py`
- `desktop-settings/cli.py`
- `desktop-installer/install.sh`
- `CMakeLists.txt`
- `desktop-packaging/glasswave-desktop.spec`
- `tests/test_config.py`

## Tests Created or Modified
- `tests/test_config.py` (added tests for `sync_to_system` command generation and mock execution).
- `tests/test_desktop_assets.py` (added checks for konsole colorscheme syntax).

## Build and Validation Results
All tests pass; CMake builds and installs successfully; module resolution verified.

## Known Limitations and Unresolved Risks
In non-KDE sessions (e.g. pure GNOME Wayland), `kwriteconfig6` safely silently succeeds or falls back gracefully without affecting the non-KDE session.

## Rollback or Recovery Procedure
`desktop-installer/uninstall.sh` restores backed-up KDE configurations using `backup_manager.py`.

## Related ADRs
- Extends [ADR-0006](0006-settings-and-control-center.md)
- Extends [ADR-0008](0008-terminal-integration.md)
- Extends [ADR-0012](0012-configuration-schema-and-migration.md)
- Extends [ADR-0013](0013-installer-and-rollback-safety.md)

## Follow-up Work
Ongoing maintenance and visual inspection in live sessions.
