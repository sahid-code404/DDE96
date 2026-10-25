# ADR-0016: Aurorae Light Window Decoration Button Assets and Symbolic Status Icons

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
The Glasswave visual design language requires complete fidelity in both Light and Dark appearance modes.
While `desktop-theme/aurorae/GlasswaveDark` provided vector SVG assets for macOS traffic light buttons (Close, Minimize, Maximize), `desktop-theme/aurorae/GlasswaveLight` lacked corresponding light-adapted SVG assets. In light mode, inactive traffic lights must render with a soft platinum gray tone (`#D1D1D6`) rather than dark graphite (`#4A4A4C`).
Additionally, `desktop-icons/Glasswave/index.theme` declared `Directories=scalable/apps,scalable/status`, but symbolic status assets were missing, limiting the visual consistency of the top menu bar and quick settings indicators.

## Scope and Requirements
1. Author pixel-aligned SVG assets for Aurorae `GlasswaveLight`:
   - `desktop-theme/aurorae/GlasswaveLight/close.svg`
   - `desktop-theme/aurorae/GlasswaveLight/minimize.svg`
   - `desktop-theme/aurorae/GlasswaveLight/maximize.svg`
2. Implement 8 symbolic scalable SVG icons under `desktop-icons/Glasswave/scalable/status/`:
   - `network-wireless-symbolic.svg`
   - `audio-volume-high-symbolic.svg`
   - `audio-volume-muted-symbolic.svg`
   - `battery-good-symbolic.svg`
   - `battery-charging-symbolic.svg`
   - `preferences-system-symbolic.svg`
   - `system-search-symbolic.svg`
   - `weather-clear-symbolic.svg`
3. Ensure all SVG files are well-formed XML and strictly conform to the 16x16 / 24x24 symbolic icon grid.
4. Maintain 100% test coverage in `tests/test_desktop_assets.py` and `tests/test_adr_coverage.py`.

## Current Behavior / Previous Implementation
- `desktop-theme/aurorae/GlasswaveLight` only contained `GlasswaveLightrc` and `metadata.json`, falling back to default or missing glyphs.
- `desktop-icons/Glasswave/scalable/status/` was non-existent.

## Decision Made
1. Author lightweight, scalable vector SVGs for `GlasswaveLight` window controls with active, hover, pressed, and inactive groups matching Aurorae specifications.
2. Author clean, minimalist symbolic SVGs conforming to the FreeDesktop Icon Naming Specification and macOS Big Sur / Sonoma geometry.

## Detailed Rationale
Aurorae requires standard element IDs (`active-center`, `hover-center`, `pressed-center`, `inactive-center`) within SVG files. Providing dedicated light mode assets ensures that inactive windows maintain proper visual contrast against light titlebars.
Dedicated symbolic icons eliminate dependency on external icon packs for core desktop indicators.

## Alternatives Evaluated
1. **Sharing dark window buttons across light and dark themes:** Rejected because dark inactive buttons on light title bars look harsh and fail macOS visual hierarchy.
2. **Relying on system Breeze status icons:** Breeze icons follow a sharp, angular aesthetic that contrasts with Glasswave's smooth, rounded squircle design language.

## Architecture and Implementation Consequences
- Window decorations in light mode now properly display soft inactive controls.
- Status indicators in the top bar and quick settings popover have dedicated symbolic assets.

## Dependencies and Version Constraints
- KWin 6.0+ Aurorae decoration engine.
- SVG 1.1 compliant vector rendering.

## Security, Performance, and Accessibility
- **Performance:** Scalable SVGs are ultra-lightweight (<1 KB each) and rasterized once into GPU texture caches.
- **Accessibility:** Traffic light colors maintain high contrast against titlebars (Red `#FF5F56`, Yellow `#FFBD2E`, Green `#27C93F`).

## Compatibility and Maintenance Implications
Assets are standard SVG files with no native binary dependencies, providing complete cross-distribution and update resilience.

## Exact List of Affected Files or Components
- `docs/adr/0016-aurorae-light-decorations-and-status-icons.md`
- `desktop-theme/aurorae/GlasswaveLight/close.svg`
- `desktop-theme/aurorae/GlasswaveLight/minimize.svg`
- `desktop-theme/aurorae/GlasswaveLight/maximize.svg`
- `desktop-icons/Glasswave/scalable/status/network-wireless-symbolic.svg`
- `desktop-icons/Glasswave/scalable/status/audio-volume-high-symbolic.svg`
- `desktop-icons/Glasswave/scalable/status/audio-volume-muted-symbolic.svg`
- `desktop-icons/Glasswave/scalable/status/battery-good-symbolic.svg`
- `desktop-icons/Glasswave/scalable/status/battery-charging-symbolic.svg`
- `desktop-icons/Glasswave/scalable/status/preferences-system-symbolic.svg`
- `desktop-icons/Glasswave/scalable/status/system-search-symbolic.svg`
- `desktop-icons/Glasswave/scalable/status/weather-clear-symbolic.svg`

## Tests Created or Modified
- `tests/test_desktop_assets.py` (validated XML well-formedness of new SVGs).

## Build and Validation Results
All SVG files pass XML parser validation and pass the test suite.

## Known Limitations and Unresolved Risks
None. Aurorae and FreeDesktop icon caches support scalable SVGs natively.

## Rollback or Recovery Procedure
Removal of the SVG files falls back to inheriting Breeze icons and Aurorae default buttons.

## Related ADRs
- Supersedes / extends [ADR-0002](0002-design-system-and-tokens.md)
- Extends [ADR-0005](0005-kwin-effects-and-window-decorations.md)

## Follow-up Work
KDE Plasma and KWin synchronization integration documented in ADR-0017.
