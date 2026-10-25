# ADR-0001: Glasswave Desktop Architecture and KDE Extension Model

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
Users seek a desktop experience that combines the visual elegance, smooth typography, translucent materials, and fluid interaction patterns of modern macOS with the flexibility, performance, and deep configuration capabilities of Linux.
Previous attempts to achieve this on Linux have typically relied on superficial icon themes, brittle CSS patches to unrelated applications, or heavy external dock utilities that lack native integration with Wayland and KWin.
Furthermore, attempts to fork desktop environments create unsustainable maintenance burdens and break across regular distribution updates.

## Scope and Requirements
1. Deliver a cohesive, high-performance desktop environment targeted at Fedora Linux with a KDE Plasma 6 Wayland session.
2. Extend KDE Plasma and KWin through supported public extension points rather than patching upstream code or maintaining a source fork.
3. Establish modular product boundaries: theme, icons, shell, effects, control center, applications suite, configuration management, installer, packaging, and tests.
4. Ensure the entire desktop environment can be installed, updated, or uninstalled reversibly without endangering existing user configurations or third-party desktop sessions (e.g. GNOME or vanilla KDE).

## Current Behavior / Previous Implementation
The initial workspace was empty (`/home/shaque/DDE96`). There was no unified project structure, no centralized branding, and no existing desktop extension integration.

## Decision Made
Adopt a modular architecture that extends KDE Plasma 6 using official extension mechanisms:
- **Global Theme (Look-and-Feel):** `org.glasswave.desktop` package managing desktop layout, Plasma style, color schemes, and window decoration defaults.
- **Plasma 6 Applets (Plasmoids):** Native QML applets for the floating dock (`org.glasswave.dock`), top menu bar (`org.glasswave.topbar`), control center popover (`org.glasswave.quicksettings`), and app launcher (`org.glasswave.launcher`).
- **KWin Integration:** Supported KWin window rules and effect configuration for backdrop blur, translucent materials, and traffic-light window button placement.
- **Shared Design Tokens:** Single source of truth in `desktop-theme/tokens.json` for semantic colors, elevation, blur radii, and motion curves.
- **Branded Applications Suite:** Native applications for files, terminal, calculator, system monitor, screenshot, and settings with consistent design language.
- **Companion Wayland Shell Runner:** Standalone Wayland client providing live preview, testability, and companion shell capabilities across sessions.
- **Idempotent Installer & Package Automation:** Comprehensive user-level and system-level installation script with automatic backup and rollback.

## Detailed Rationale
Extending KDE Plasma 6 via standard KPackage specifications, Aurorae window decorations, and Plasma applets guarantees:
1. Long-term update resilience when Fedora upgrades Plasma 6 minor releases.
2. Complete session stability without risky C++ binary injection into kwin or plasmashell.
3. Clean separation between user preferences and system defaults.

## Alternatives Evaluated
1. **Forking Plasma Shell / KWin:** Rejected due to prohibitive maintenance overhead, risk of breaking with upstream Fedora updates, and security implications.
2. **GNOME Shell Extension Suite:** Evaluated, but GNOME Shell extension APIs break frequently across GNOME releases (e.g. 45 -> 51), whereas KDE Plasma 6 provides stable declarative KPackage interfaces.
3. **Stand-alone Window Manager (e.g. Hyprland / Sway):** Rejected because the task requires a complete, mature desktop environment with standard display settings, multi-monitor handling, desktop activities, and power management.

## Architecture and Implementation Consequences
- Components communicate via standard FreeDesktop standards, D-Bus, and XDG specifications.
- Clean dependency management: the desktop runs with standard Qt 6, KDE Frameworks 6, Python 3, GTK 4, and Wayland protocols.

## Dependencies and Version Constraints
- Target OS: Fedora Linux 45 (or 40+) x86_64.
- KDE Plasma 6.0+ / KDE Frameworks 6.0+.
- Qt 6.6+.
- Python 3.10+.
- Wayland compositor (KWin Wayland or Wayland layer-shell compositor).

## Security, Performance, and Accessibility
- **Security:** No setuid binaries, no sudo requirement for user-level installation, no plain-text credentials stored.
- **Performance:** Hardware-accelerated rendering, no polling loops, asynchronous system monitoring.
- **Accessibility:** High-contrast color tokens, full keyboard navigation support, and full support for reduced-motion preferences.

## Exact List of Affected Files
- `.gitignore`
- `CMakeLists.txt`
- `Makefile`
- `CHECKLIST.md`
- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `docs/architecture/overview.md`
- `docs/architecture/data-flow.md`
- `docs/development/building.md`
- `docs/compatibility.md`
- `docs/security.md`
- `docs/adr/0001-project-architecture.md`

## Tests Created or Modified
- `tests/test_adr_coverage.py`
- `tests/test_desktop_assets.py`

## Build and Validation Results
- Initial architecture validated; directories and documentation structured according to project specification.

## Known Limitations and Unresolved Risks
- KDE Plasma 6 Wayland session features require a running Plasma session to test full native applet docking, but the standalone Wayland companion shell enables immediate visual and functional verification on any Wayland compositor.

## Rollback or Recovery Procedure
- Revert repository state via `git checkout` or restore backed-up configurations via `desktop-installer/uninstall.sh`.

## Related ADRs
- Precedes ADR-0002 through ADR-0015.
