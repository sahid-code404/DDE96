# ADR-0002: Centralized Design System, Tokens, and Materials

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
A desktop environment inspired by macOS requires strict visual harmony: consistent surface translucency, corner radii, drop shadows, semantic color roles, typography scales, and motion curves.
Scattering arbitrary hex codes, margin values, and animation durations across QML files, CSS sheets, and Python scripts causes visual degradation and makes theme customization fragile.

## Scope and Requirements
1. Centralize all visual tokens in machine-readable JSON formats (`desktop-theme/tokens.json` and `desktop-theme/branding.json`).
2. Provide light and dark palettes with balanced contrast (WCAG AA compliant for core text and controls).
3. Specify frosted glass materials with fallback opaque values for environments with disabled compositor blur or high-contrast mode.
4. Support reduced-motion mode by defining animation durations as zero or minimal when motion is suppressed.

## Current Behavior / Previous Implementation
No centralized design tokens existed. Standard KDE themes rely on scattered INI and SVG files with fixed color values.

## Decision Made
1. Author `desktop-theme/branding.json` to centralize product name, tagline, vendor identifier, and asset directories.
2. Author `desktop-theme/tokens.json` defining:
   - **Semantic Colors:** Primary accent (`#0A84FF`), secondary accent (`#5E5CE6`), success (`#30D158`), warning (`#FF9F0A`), destructive (`#FF453A`), background tints, text hierarchy.
   - **Materials & Translucency:** Frosted glass surface styles with backdrop filters, surface opacity (0.78 for panels, 0.85 for popovers, 0.92 for modals).
   - **Corner Radii:** S (6px), M (10px), L (16px), XL (22px), Dock (24px).
   - **Shadows:** Elevation levels 1 to 4 with refined ambient and directional spread.
   - **Typography:** Hierarchy from Caption (11px) to Display (28px) with proportional line heights.
   - **Motion:** Standard easing (`cubic-bezier(0.2, 0.0, 0.0, 1.0)`), normal duration (200ms), fast (120ms), and reduced motion override (0ms).

## Detailed Rationale
A single JSON token repository allows QML, Python/GTK, and CSS components to import or generate their styles programmatically, ensuring 100% visual parity across cross-toolkit applications.

## Alternatives Evaluated
1. **Hardcoding values inside QML components:** Rejected because it violates maintainability and prevents centralized rebranding.
2. **CSS variables only:** Rejected because pure Qt/QML and KWin scripts cannot natively ingest standard web CSS files without external parsing.

## Architecture and Implementation Consequences
All UI components, whether rendered in Qt QML or Python/GTK, query the centralized design token provider or generated theme files.

## Dependencies and Version Constraints
None; JSON is standard and readable across all languages.

## Security, Performance, and Accessibility
- **Performance:** Pre-computed static tokens prevent runtime style recalculation.
- **Accessibility:** Semantic tokens include dedicated high-contrast fallbacks and reduced-motion timing flags.

## Exact List of Affected Files
- `desktop-theme/branding.json`
- `desktop-theme/tokens.json`
- `docs/design/design-system.md`
- `docs/design/interaction-guidelines.md`
- `docs/adr/0002-design-system-and-tokens.md`

## Tests Created or Modified
- `tests/test_desktop_assets.py` (validates JSON token schema and completeness)

## Build and Validation Results
Tokens validated against JSON schema and verified for contrast ratios.

## Known Limitations and Unresolved Risks
Applications running in strict isolated sandbox environments (Flatpak without filesystem access) will use their packaged fallback tokens.

## Rollback or Recovery Procedure
Tokens can be updated or reverted without touching application logic.

## Related ADRs
- Related to ADR-0001 (Architecture) and ADR-0003 (Plasma Theme).
