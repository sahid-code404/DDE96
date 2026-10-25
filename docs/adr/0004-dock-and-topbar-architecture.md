# ADR-0004: Floating Dock and Top Bar Shell Architecture

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
The signature interaction model of macOS centers on two complementary elements:
1. A slim, persistent top menu bar containing the brand/apple menu, active application title, global menu when available, and system status indicators.
2. A floating bottom dock with smooth pointer magnification, running application dots, active application bounce/glow, pinned application persistence, and context menus.
In KDE Plasma 6, panels can be customized natively via QML applets (plasmoids) and panel floating settings. However, to guarantee cross-session testability and live previews even when the Plasma shell is not running (e.g. during headless CI or standalone Wayland testing), a companion shell runner is also essential.

## Scope and Requirements
1. Implement native Plasma 6 QML plasmoids:
   - `org.glasswave.dock`: macOS-style floating dock applet supporting item magnification, running indicators, pinned apps, and drag-and-drop ordering.
   - `org.glasswave.topbar`: Top bar applet featuring brand mark, active application name, date/time, and quick settings toggle.
   - `org.glasswave.quicksettings`: Compact control center popover for Wi-Fi, Bluetooth, volume slider, brightness slider, dark mode toggle, and Do Not Disturb.
   - `org.glasswave.launcher`: Full-screen/modal spotlight launcher with search, category filtering, and keyboard navigation.
2. Implement a companion Wayland shell runner (`desktop-shell/companion/shell_companion.py`) capable of running standalone on Wayland or X11 to verify the dock and top bar visually and interactively.

## Current Behavior / Previous Implementation
No dock or top bar plasmoids existed for Glasswave. Standard KDE default is a single bottom panel with Task Manager and System Tray.

## Decision Made
1. Author QML applets adhering to the Plasma 6 Applet API (`import org.kde.plasma.plasmoid 2.0`, `import org.kde.plasma.core as PlasmaCore`, `import org.kde.kirigami as Kirigami`):
   - `desktop-shell/plasmoids/org.glasswave.dock/`
   - `desktop-shell/plasmoids/org.glasswave.topbar/`
   - `desktop-shell/plasmoids/org.glasswave.quicksettings/`
   - `desktop-shell/plasmoids/org.glasswave.launcher/`
2. Implement magnification math using a cosine-weighted bell curve centered on the hovered item index with configurable max zoom (1.0 to 1.7x).
3. Author `desktop-shell/companion/shell_companion.py` using GTK 4 / Wayland / Layer-Shell bindings that renders the exact Glasswave dock and top bar surfaces with real process launching, time display, and control center toggles.

## Detailed Rationale
Dual-mode availability ensures that users running KDE Plasma 6 get native plasmoids integrated directly into KWin and Plasma panels, while developers and CI environments can immediately launch, test, and visually inspect the shell via the companion runner.

## Alternatives Evaluated
1. **Plank / Cairo-Dock:** Plank is GTK3 X11-only and completely broken on Wayland. Cairo-Dock is unmaintained and crash-prone on modern Wayland compositors.
2. **Latte Dock:** Abandoned by upstream authors, incompatible with Plasma 6 and Qt 6.

## Architecture and Implementation Consequences
- The dock communicates with the system via FreeDesktop `.desktop` files and DBus interfaces (`org.freedesktop.Application`).
- Settings for pinned applications and magnification are stored in the centralized `~/.config/glasswave/glasswave.json` and mirrored in Plasma applet configs.

## Dependencies and Version Constraints
- Plasma 6.0+ QML runtime or Python 3 + GTK 4 / Cairo for the companion runner.
- Wayland layer-shell protocol when running standalone on Wayland.

## Security, Performance, and Accessibility
- **Performance:** Magnification uses GPU-accelerated transforms rather than re-rasterizing SVG textures on every hover frame.
- **Accessibility:** Full keyboard traversal (arrow keys navigate dock items, Return launches, Escape dismisses popovers).

## Exact List of Affected Files
- `desktop-shell/plasmoids/org.glasswave.dock/metadata.json`
- `desktop-shell/plasmoids/org.glasswave.dock/contents/ui/main.qml`
- `desktop-shell/plasmoids/org.glasswave.dock/contents/ui/DockItem.qml`
- `desktop-shell/plasmoids/org.glasswave.dock/contents/ui/DockConfig.qml`
- `desktop-shell/plasmoids/org.glasswave.topbar/metadata.json`
- `desktop-shell/plasmoids/org.glasswave.topbar/contents/ui/main.qml`
- `desktop-shell/plasmoids/org.glasswave.quicksettings/metadata.json`
- `desktop-shell/plasmoids/org.glasswave.quicksettings/contents/ui/main.qml`
- `desktop-shell/plasmoids/org.glasswave.launcher/metadata.json`
- `desktop-shell/plasmoids/org.glasswave.launcher/contents/ui/main.qml`
- `desktop-shell/companion/__init__.py`
- `desktop-shell/companion/shell_companion.py`
- `docs/adr/0004-dock-and-topbar-architecture.md`

## Tests Created or Modified
- `tests/test_desktop_assets.py` (validates plasmoid metadata and QML structure)
- Shell companion headless sanity execution

## Build and Validation Results
Applet metadata and QML structures validated; shell companion executes and renders surfaces cleanly.

## Known Limitations and Unresolved Risks
In pure Plasma 6 Wayland, global menus depend on application toolkit support (Qt and GTK with `appmenu-gtk-module`). Applications lacking DBus menu export fall back to their local in-window menubar.

## Rollback or Recovery Procedure
Remove plasmoids from `~/.local/share/plasma/plasmoids/` or reset Plasma panels using `plasma-org.kde.plasma.desktop-appletsrc` backup.

## Related ADRs
- Related to ADR-0001, ADR-0003, and ADR-0006.
