# ADR-0006: Glasswave Settings and Appearance Center

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
Users require a dedicated, polished configuration center reminiscent of macOS System Settings.
The application must provide an intuitive interface to control desktop themes, light/dark mode, accent colors, dock sizing and magnification, top bar appearance, window decorations, blur/transparency levels, and accessibility options (reduced motion).
Furthermore, it must feature real configuration persistence, schema validation, configuration backup/export/import, and rollback capabilities—without corrupting existing KDE settings.

## Scope and Requirements
1. Build `glasswave-settings` (`desktop-control-center/control_center.py`) with a modern macOS-inspired two-pane layout (category sidebar + detailed preference pane).
2. Support sections:
   - **Appearance:** Light / Dark mode toggle, 6 accent colors (Blue, Purple, Pink, Orange, Green, Graphite), wallpaper selection.
   - **Dock:** Icon size slider (32px to 96px), magnification factor (1.0x to 1.8x), position (Bottom, Left, Right), autohide mode.
   - **Top Bar:** Spacing, clock format (12h/24h), active application title display toggle.
   - **Window Decorations:** Button placement (Left / Right), shadow intensity.
   - **Effects & Materials:** Blur strength slider, surface translucency slider, opaque fallback toggle.
   - **Accessibility & Motion:** Animation speed slider, Reduced Motion toggle (disables all nonessential motion).
   - **Backup & Reset:** Export configuration, Import configuration, Reset to Glasswave defaults, Restore original KDE session.
   - **System Info & Diagnostics:** OS, kernel, compositor, Wayland status, CPU/RAM summary.
3. Integrate with the central configuration manager (`desktop-settings/settings_manager.py`).

## Current Behavior / Previous Implementation
No dedicated Glasswave settings center existed. System settings were split across default KDE System Settings modules without Glasswave-specific tuning.

## Decision Made
1. Implement `glasswave-settings` in Python with GTK 4 / Libadwaita and custom Glasswave CSS styling, leveraging the available `gi.repository.Adw` and `Gtk` modules.
2. Connect UI controls directly to `SettingsManager` which persists settings to `~/.config/glasswave/glasswave.json` with strict schema validation.
3. Automatically apply underlying KDE configuration changes (e.g. updating `kwinrc`, `kdeglobals`, and Plasma color schemes) when the user modifies appearance settings.
4. Support headless CLI operations via `desktop-settings/cli.py` for automated testing and scripting.

## Detailed Rationale
GTK 4 / Libadwaita provides high-performance rendering, Wayland fractional scaling, touch and touchpad gesture support, and an elegant sidebar navigation pattern that closely mirrors macOS System Settings. Backed by `SettingsManager`, changes take effect immediately and are stored safely.

## Alternatives Evaluated
1. **Writing a pure Qt/QML application:** Evaluated; however, the build environment lacks `PyQt6` and `qt6-qtdeclarative-devel` compilers. Python + GTK 4 / Libadwaita is fully functional on the host with native introspection (`gi.repository.Gtk` 4.0 and `Adw` 1.0) and renders natively on Wayland.
2. **KCM (KDE Control Module) plugin only:** A pure KCM plugin would not be visible or usable outside KDE System Settings and cannot provide a standalone branded experience.

## Architecture and Implementation Consequences
- Provides desktop entry `org.glasswave.settings.desktop`.
- Reads and updates `~/.config/glasswave/glasswave.json`.
- Can be launched directly from the dock, top bar, application launcher, or CLI (`glasswave-settings`).

## Dependencies and Version Constraints
- Python 3.10+
- `gi.repository.Gtk` (4.0)
- `gi.repository.Adw` (1.0)

## Security, Performance, and Accessibility
- **Security:** Modifies only user-scoped settings files; never requires root permissions.
- **Performance:** Lightweight process with fast startup (<200ms); event-driven updates without polling loops.
- **Accessibility:** Full keyboard navigation (`Tab`, arrow keys, shortcuts) and ARIA accessibility roles.

## Exact List of Affected Files
- `desktop-control-center/__init__.py`
- `desktop-control-center/control_center.py`
- `desktop-control-center/org.glasswave.settings.desktop`
- `desktop-settings/__init__.py`
- `desktop-settings/schema.json`
- `desktop-settings/settings_manager.py`
- `desktop-settings/cli.py`
- `docs/troubleshooting.md`
- `docs/adr/0006-settings-and-control-center.md`

## Tests Created or Modified
- `tests/test_config.py` (unit tests for SettingsManager, schema validation, import/export, reset)
- CLI headless test suite execution

## Build and Validation Results
Settings manager and control center pass all automated unit tests and schema verification.

## Known Limitations and Unresolved Risks
Live preview of KWin window decoration changes requires KWin to re-read configuration (`qdbus org.kde.KWin /KWin reconfigure` or session reload).

## Rollback or Recovery Procedure
Execute `glasswave-config reset` or restore a prior backup via `glasswave-config restore <backup-file>`.

## Related ADRs
- Related to ADR-0001, ADR-0002, ADR-0012, and ADR-0013.
