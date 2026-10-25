# ADR-0003: Plasma 6 Look-and-Feel, Styles, and Color Schemes

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
KDE Plasma requires specific packaging structures to register global themes, color schemes, Plasma styles, and desktop layouts.
For Plasma 6, metadata is defined in `metadata.json` (replacing the deprecated Plasma 5 `metadata.desktop`), and color schemes follow the standard KDE color format (`.colors`).
Without genuine Plasma 6 packages, the desktop cannot be selected in KDE System Settings or applied atomically via `lookandfeeltool`.

## Scope and Requirements
1. Implement native Plasma 6 Global Theme `org.glasswave.desktop` containing metadata, default configurations, and automated layout script.
2. Implement Light and Dark KDE color schemes: `GlasswaveDark.colors` and `GlasswaveLight.colors`.
3. Implement custom Plasma Style SVG assets (`panel-background.svg`, `background.svg`) delivering frosted translucent surfaces with subtle glass borders.
4. Provide original scalable vector wallpapers (`3840x2160.svg`, `3840x2160-light.svg`).
5. Deliver custom icon theme structure (`desktop-icons/Glasswave`) with macOS-inspired squircles and FreeDesktop `index.theme`.

## Current Behavior / Previous Implementation
The system lacked Glasswave look-and-feel packages. Default KDE packages only contained standard Breeze and Oxygen assets.

## Decision Made
1. Author `desktop-theme/plasma-look-and-feel/org.glasswave.desktop/metadata.json` adhering to Plasma 6 specifications.
2. Author `contents/defaults` specifying:
   - ColorScheme=GlasswaveDark
   - LookAndFeelPackage=org.glasswave.desktop
   - Theme=org.glasswave.desktop (Plasma Style)
   - widgetStyle=Breeze
   - icons=Glasswave
   - cursorTheme=breeze_cursors
3. Author `contents/layouts/org.glasswave.desktop.layout/contents/layout.js` to configure the default macOS dual-panel layout:
   - Panel 1: Slim top bar with Global Menu, active task title, system tray, clock, and Glasswave Control Center trigger.
   - Panel 2: Floating bottom dock with centered task manager and quick launchers.
4. Author standard KDE color scheme files with frosted background palettes:
   - Dark: Background `#1c1c1e`, Window `#2c2c2e`, Selection `#0a84ff`.
   - Light: Background `#f5f5f7`, Window `#ffffff`, Selection `#007aff`.
5. Author vector SVG wallpapers and icon theme assets.

## Detailed Rationale
Using the native Plasma 6 Look-and-Feel format allows instantaneous, one-click application and full integration with KDE's session initialization.

## Alternatives Evaluated
1. **Ad-hoc shell script replacing user config files blindly:** Rejected because directly overwriting `plasma-org.kde.plasma.desktop-appletsrc` while `plasmashell` is running causes corruption and race conditions.
2. **Third-party layout managers (e.g. Latte Dock layouts):** Rejected because Latte Dock is unmaintained and incompatible with Plasma 6 Wayland.

## Architecture and Implementation Consequences
- Provides seamless installation into `~/.local/share/plasma/look-and-feel/` (user) or `/usr/share/plasma/look-and-feel/` (system).
- Completely reversible via standard KDE System Settings.

## Dependencies and Version Constraints
- Plasma 6.0+ (compatible with verified Fedora 45 Plasma 6.7.5 packages).
- KDE Frameworks 6.0+.

## Security, Performance, and Accessibility
- Assets are pure declarative JSON, INI, and SVG files with zero arbitrary executable code.
- SVGs are optimized for GPU rasterization without complex filters that stress the compositor.

## Exact List of Affected Files
- `desktop-theme/color-schemes/GlasswaveDark.colors`
- `desktop-theme/color-schemes/GlasswaveLight.colors`
- `desktop-theme/plasma-look-and-feel/org.glasswave.desktop/metadata.json`
- `desktop-theme/plasma-look-and-feel/org.glasswave.desktop/contents/defaults`
- `desktop-theme/plasma-look-and-feel/org.glasswave.desktop/contents/layouts/org.glasswave.desktop.layout/contents/layout.js`
- `desktop-theme/plasma-style/org.glasswave.desktop/metadata.json`
- `desktop-theme/plasma-style/org.glasswave.desktop/contents/widgets/panel-background.svg`
- `desktop-theme/plasma-style/org.glasswave.desktop/contents/widgets/background.svg`
- `desktop-theme/wallpapers/metadata.json`
- `desktop-theme/wallpapers/contents/images/3840x2160.svg`
- `desktop-theme/wallpapers/contents/images/3840x2160-light.svg`
- `desktop-icons/Glasswave/index.theme`
- `desktop-icons/Glasswave/scalable/apps/glasswave-files.svg`
- `desktop-icons/Glasswave/scalable/apps/glasswave-terminal.svg`
- `desktop-icons/Glasswave/scalable/apps/glasswave-settings.svg`
- `desktop-icons/Glasswave/scalable/apps/glasswave-calculator.svg`
- `desktop-icons/Glasswave/scalable/apps/glasswave-monitor.svg`
- `desktop-icons/Glasswave/scalable/apps/glasswave-screenshot.svg`
- `docs/adr/0003-plasma-theme-and-color-schemes.md`

## Tests Created or Modified
- `tests/test_desktop_assets.py` (validates color scheme INI parsing, layout.js syntax, metadata.json schemas, SVG integrity)

## Build and Validation Results
All assets pass syntax validation, XML parsing, and JSON schema checks.

## Known Limitations and Unresolved Risks
Third-party GTK applications without CSS support fall back to Breeze-GTK or Adwaita themes.

## Rollback or Recovery Procedure
Revert to Breeze theme via `lookandfeeltool -a org.kde.breezedark.desktop`.

## Related ADRs
- Preceded by ADR-0001, ADR-0002; related to ADR-0004 (Dock).
