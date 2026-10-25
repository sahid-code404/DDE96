# ADR-0011: Wayland Screenshot Utility via XDG Desktop Portal (glasswave-screenshot)

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
macOS provides an iconic floating screenshot utility (triggered via `Cmd+Shift+4` or `Cmd+Shift+5`) featuring a pill-shaped control bar with capture modes (Full Screen, Window, Selection), delay options, and direct preview thumbnail.
On modern Wayland (Fedora KDE Wayland), applications cannot arbitrarily grab pixel buffers of other windows due to Wayland security isolation.
The only secure, standard mechanism for taking screenshots on Wayland is the FreeDesktop XDG Desktop Portal (`org.freedesktop.portal.Screenshot` and `org.freedesktop.portal.ScreenCast`), or delegating to the compositor's trusted capture utility (such as KDE Spectacle).

## Scope and Requirements
1. Build `glasswave-screenshot` (`desktop-apps/screenshot/screenshot.py`):
   - macOS-inspired floating pill HUD HUD overlay with rounded glass design and drop shadow.
   - Capture modes: Full Screen, Active Window, Selected Region.
   - Options: Delay timer (0s, 3s, 5s, 10s), Include pointer cursor toggle.
   - Actions: Save to file (`~/Pictures/Screenshots/`), Copy to Clipboard, Annotate / Edit in KDE Spectacle.
2. Implement portal-first capture architecture:
   - Queries `org.freedesktop.portal.Desktop` via DBus.
   - Falls back gracefully to `spectacle --background --nonotify` or CLI capture if portal is unavailable.
   - Never attempts insecure X11 root-window grabs on Wayland.
3. Provide desktop entry `org.glasswave.screenshot.desktop`.

## Current Behavior / Previous Implementation
No custom Glasswave screenshot HUD existed. Standard KDE tool is Spectacle.

## Decision Made
1. Develop `glasswave-screenshot` using Python 3 and GTK 4 / Libadwaita with frosted pill HUD styling.
2. Interface with `org.freedesktop.portal.Screenshot` over DBus to request secure Wayland captures with user consent and portal sandbox guarantees.
3. Maintain seamless integration with KDE Spectacle for advanced image annotation and cloud export.

## Detailed Rationale
Using the XDG Desktop Portal guarantees security, compliance with Wayland isolation policies, and full compatibility across both KDE Wayland and GNOME Wayland sessions.

## Alternatives Evaluated
1. **Using X11 XGetImage / XCopyArea:** Completely fails on native Wayland windows or captures only Xwayland windows.
2. **Unsupported KWin internal memory hacks:** Extremely brittle; violates system security and breaks with KWin updates.

## Architecture and Implementation Consequences
- Provides `glasswave-screenshot` executable and desktop entry.
- Fully respects Wayland security boundary.

## Dependencies and Version Constraints
- FreeDesktop XDG Desktop Portal (`xdg-desktop-portal` and `xdg-desktop-portal-kde` or `xdg-desktop-portal-gnome`).
- Python 3.10+
- `gi.repository.Gtk` (4.0)

## Security, Performance, and Accessibility
- **Security:** Standard portal mediation guarantees that the user is always informed of screenshot captures.
- **Performance:** Instant HUD activation; low memory footprint.
- **Accessibility:** Full keyboard shortcut bindings (`Esc` to dismiss, `Space` or `Return` to capture).

## Exact List of Affected Files
- `desktop-apps/screenshot/__init__.py`
- `desktop-apps/screenshot/screenshot.py`
- `desktop-apps/screenshot/org.glasswave.screenshot.desktop`
- `docs/adr/0011-screenshot-and-portals.md`

## Tests Created or Modified
- `tests/test_desktop_assets.py` (validates desktop entry and asset metadata)
- Portal detection and CLI option unit tests

## Build and Validation Results
Screenshot utility loads cleanly, parses portal parameters, and executes fallback pathways safely.

## Known Limitations and Unresolved Risks
Region selection in pure Wayland requires compositor portal support (`xdg-desktop-portal-kde` handles the interactive crosshair overlay).

## Rollback or Recovery Procedure
Revert default screenshot tool to Spectacle via `xdg-mime default org.kde.spectacle.desktop`.

## Related ADRs
- Related to ADR-0001, ADR-0002, and ADR-0012.
