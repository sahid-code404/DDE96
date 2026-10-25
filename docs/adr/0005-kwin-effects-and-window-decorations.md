# ADR-0005: KWin Window Decorations, Blur, and Effects Rules

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
A genuine macOS desktop look requires:
1. Window titlebars with left-aligned circular "traffic light" controls (Close `#FF5F56`, Minimize `#FFBD2E`, Maximize/Zoom `#27C93F`).
2. Rounded window corners and delicate drop shadows.
3. Translucent frosted glass effect on supported application surfaces (sidebars, toolbars) without excessive GPU load or visual artifacts over bright backgrounds.
4. Window management rules that apply consistent decoration policies across traditional server-side decorated (SSD) and client-side decorated (CSD) windows.

## Scope and Requirements
1. Implement Aurorae window decoration themes: `GlasswaveDark` and `GlasswaveLight`.
2. Configure KWin decoration rules (`kwinrc` snippets) setting button placement to left: `ButtonsOnLeft=XIA`, `ButtonsOnRight=`.
3. Provide KWin blur effect settings (`kwinrc` `[Plugins]` and `[Effect-blur]`) configured for high visual quality with smooth downscaling and noise reduction.
4. Provide window rules (`kwinrulesrc.glasswave`) for Glasswave apps, setting appropriate opacity and geometry rules.
5. Provide a KWin script / effect configuration for macOS-style Mission Control workspace overview and smooth window switching.

## Current Behavior / Previous Implementation
No custom window decoration or KWin configuration existed. Default KDE uses Breeze window decoration with right-aligned minimize, maximize, and close buttons.

## Decision Made
1. Author Aurorae decoration packages:
   - `desktop-theme/aurorae/GlasswaveDark/`: `GlasswaveDarkrc`, SVG button definitions for close, minimize, maximize with hover/press states.
   - `desktop-theme/aurorae/GlasswaveLight/`: `GlasswaveLightrc`, corresponding light assets.
2. Author `desktop-effects/kwinrc.glasswave` defining:
   - `[org.kde.kdecoration2]` plugin=org.kde.kwin.aurorae, theme=GlasswaveDark, `ButtonsOnLeft=XIA`, `ButtonsOnRight=`.
   - `[Effect-blur]` BlurStrength=8, NoiseStrength=2.
   - `[Windows]` BorderlessMaximizedWindows=false, ElectricBorders=0.
3. Author `desktop-effects/kwinrulesrc.glasswave` specifying window rules for Glasswave Terminal and File Manager to enable translucency and rounded geometry.
4. Author `desktop-effects/scripts/org.glasswave.overview/` KWin script for Mission Control overview activation.

## Detailed Rationale
Aurorae is KDE's official declarative SVG window decoration engine. It is fully supported in Plasma 6, runs securely inside KWin without compiling native C++ decoration plugins, and allows pixel-perfect traffic light styling with complete DPI scaling.

## Alternatives Evaluated
1. **Compiling a native C++ KDecoration2 plugin:** High risk of ABI breakage between minor KDE releases (e.g. Plasma 6.2 vs 6.3) and requires development headers that may not be available on all end-user machines.
2. **Forcing GTK CSD on all KDE windows:** Incompatible with native Qt/KDE applications and causes broken window shadows on Wayland.

## Architecture and Implementation Consequences
- The decoration theme is installed into `~/.local/share/aurorae/themes/` or `/usr/share/aurorae/themes/`.
- Window rules integrate smoothly with existing user rules via KWin's rule merging logic.

## Dependencies and Version Constraints
- KWin 6.0+ Wayland or X11.

## Security, Performance, and Accessibility
- **Performance:** Aurorae SVG rendering is cached in GPU memory; blur uses KWin's built-in dual-filtering blur shader.
- **Accessibility:** High-contrast border definitions ensure windows remain clearly distinguishable against dark or busy wallpapers.

## Exact List of Affected Files
- `desktop-theme/aurorae/GlasswaveDark/metadata.json`
- `desktop-theme/aurorae/GlasswaveDark/GlasswaveDarkrc`
- `desktop-theme/aurorae/GlasswaveDark/close.svg`
- `desktop-theme/aurorae/GlasswaveDark/minimize.svg`
- `desktop-theme/aurorae/GlasswaveDark/maximize.svg`
- `desktop-theme/aurorae/GlasswaveLight/metadata.json`
- `desktop-theme/aurorae/GlasswaveLight/GlasswaveLightrc`
- `desktop-effects/kwinrc.glasswave`
- `desktop-effects/kwinrulesrc.glasswave`
- `desktop-effects/scripts/org.glasswave.overview/metadata.json`
- `desktop-effects/scripts/org.glasswave.overview/contents/code/main.js`
- `docs/adr/0005-kwin-effects-and-window-decorations.md`

## Tests Created or Modified
- `tests/test_desktop_assets.py` (validates decoration configs, metadata, and SVG syntax)

## Build and Validation Results
All Aurorae configuration files and SVGs pass syntax and format validation.

## Known Limitations and Unresolved Risks
Some client-side decorated applications (e.g. certain Chromium builds or GNOME apps) render their own titlebars; our GTK 4 / Libadwaita theme settings configure these to also align buttons to the left.

## Rollback or Recovery Procedure
Restore default Breeze window decoration using `kwriteconfig6 --file kwinrc --group "org.kde.kdecoration2" --key "theme" "Breeze"`.

## Related ADRs
- Related to ADR-0001, ADR-0002, ADR-0003, and ADR-0013.
