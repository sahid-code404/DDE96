# Changelog

All notable changes to Glasswave Desktop will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-26

### Added
- **Core Architecture & Design Tokens:**
  - Centralized branding in `desktop-theme/branding.json` and tokens in `desktop-theme/tokens.json`.
  - Light and Dark KDE color schemes: `GlasswaveDark.colors` and `GlasswaveLight.colors`.
  - Plasma 6 Look-and-Feel package `org.glasswave.desktop` with automated dual-panel layout script.
  - Plasma Style SVG surfaces with frosted glass borders and transparency.
  - Aurorae window decoration themes `GlasswaveDark` and `GlasswaveLight` with left-aligned traffic-light buttons.
  - Original scalable vector wallpapers in dark and light variants.
  - Cohesive squircle icon theme (`Glasswave`) with custom application and status icons.
- **Desktop Shell & Plasmoids:**
  - Plasma 6 QML floating dock plasmoid (`org.glasswave.dock`) with pointer magnification, running indicators, and launch bounce.
  - Plasma 6 Top Bar plasmoid (`org.glasswave.topbar`) with active window title and indicators.
  - Plasma 6 Quick Settings popover (`org.glasswave.quicksettings`) for Wi-Fi, Bluetooth, volume, and brightness.
  - Application launcher plasmoid (`org.glasswave.launcher`) with search and category filtering.
  - Standalone Wayland companion shell runner (`desktop-shell/companion/shell_companion.py`) for live desktop testing.
- **Applications Suite:**
  - Finder-inspired File Manager (`glasswave-files`): sidebar, breadcrumbs, list/grid views, search, Quick Look, and trash integration.
  - Translucent Terminal (`glasswave-terminal`): frosted glass styling, tabs, search, and Konsole theme integration.
  - Safe Calculator (`glasswave-calculator`): macOS layout, AST-based safe evaluation engine, calculation history.
  - System Activity Monitor (`glasswave-monitor`): real-time `/proc` metrics and process manager with honest permissions.
  - Screenshot HUD (`glasswave-screenshot`): floating pill HUD for full-screen, window, and region capture via XDG Desktop Portal.
- **Settings & Configuration:**
  - Glasswave Settings & Appearance Center (`glasswave-settings`).
  - Schema-validated configuration manager (`SettingsManager`) with atomic writes and automated backups.
  - CLI utility `glasswave-config` for scripted administration.
- **Installation & Packaging:**
  - Idempotent installer (`desktop-installer/install.sh`) supporting user and system modes.
  - Full uninstaller (`desktop-installer/uninstall.sh`) with restoration of backed-up KDE configurations.
  - Fedora RPM specification file (`desktop-packaging/glasswave-desktop.spec`) and build automation.
- **Testing & Documentation:**
  - Automated test suite covering config schema, calculator AST security, file operations, system monitor, installer, and assets.
  - Automated ADR coverage audit (`tests/test_adr_coverage.py`).
  - Complete documentation suite and 17 Architecture Decision Records (ADRs).
- **KDE System Settings & Asset Refinements:**
  - Aurorae Light window decoration SVG assets for traffic lights.
  - Scalable vector symbolic status icons (Wi-Fi, Audio, Battery, System, Search, Weather).
  - Direct two-way sync to KDE Plasma 6 (`kdeglobals`, `kwinrc`) via `kwriteconfig6` and D-Bus.
  - Direct launchers for native KDE Control Modules (`kcmshell6`).
  - Standalone module search paths for robust post-installation execution.
