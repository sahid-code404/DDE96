# Glasswave Desktop Implementation Checklist

## 1. Initial Investigation and Environment
- [x] Identify Git repository, OS (Fedora 45 Linux x86_64, Wayland session `wayland-0`).
- [x] Identify installed dependencies: GCC 16, CMake 4.3, Python 3.15, Qt 6.11, KF6 6.31, GTK4 4.24, Cairo, Wayland client/server devel.
- [x] Establish ADR documentation workflow with mandatory ADR mapping for every change.

## 2. Core Architecture & Design System
- [x] Centralized branding configuration (`desktop-theme/branding.json`).
- [x] Design tokens: semantic colors, glass materials, typography, radii, spacing (`desktop-theme/tokens.json`).
- [x] Light and Dark color schemes for KDE / Qt (`GlasswaveLight.colors`, `GlasswaveDark.colors`).
- [x] Plasma 6 Look-and-Feel package (`org.glasswave.desktop`).
- [x] Plasma Style SVG assets with frosted glass translucent textures.
- [x] Window decorations (Aurorae theme `GlasswaveDark`, `GlasswaveLight` with traffic light buttons).
- [x] Original vector wallpapers (`3840x2160.svg`, `3840x2160-light.svg`).
- [x] Cohesive icon theme (`desktop-icons/Glasswave`) with squircle app icons and symbolic status indicators.

## 3. Desktop Shell & KWin Integration
- [x] Plasma 6 Dock plasmoid (`org.glasswave.dock`) with hover magnification, running indicators, pinned apps.
- [x] Plasma 6 Top Bar plasmoid (`org.glasswave.topbar`) with active window title and system indicators.
- [x] Plasma 6 Quick Settings Control Center popover (`org.glasswave.quicksettings`).
- [x] Application Launcher (`org.glasswave.launcher`) with category & fuzzy search.
- [x] Standalone Wayland shell companion for live desktop testing and preview (`desktop-shell/companion`).
- [x] KWin window rules and blur configuration (`desktop-effects`).

## 4. Control Center & Applications Suite
- [x] Glasswave Settings & Appearance Center (`desktop-control-center` / `glasswave-settings`).
- [x] Finder-inspired File Manager (`glasswave-files`): breadcrumbs, sidebar, list/grid views, safe file operations, trash integration, search.
- [x] Translucent Terminal (`glasswave-terminal`): frosted styling, tabs, search, shell integration.
- [x] Safe Calculator (`glasswave-calculator`): macOS UI, AST-based safe evaluation engine, history.
- [x] System Monitor (`glasswave-monitor`): CPU/RAM/Disk metrics, process manager with honest permissions.
- [x] Screenshot HUD (`glasswave-screenshot`): full-screen, window, region capture via XDG Desktop Portal.

## 5. Configuration, Packaging, & Safety
- [x] JSON Schema validated configuration system (`desktop-settings/schema.json`, `settings_manager.py`, `cli.py`).
- [x] Safe idempotent installer (`desktop-installer/install.sh`) supporting `--user` and `--system`.
- [x] Safe uninstaller (`desktop-installer/uninstall.sh`) with full restoration of backed up KDE settings.
- [x] Backup manager (`desktop-installer/backup_manager.py`).
- [x] Fedora RPM spec file (`desktop-packaging/glasswave-desktop.spec`) and build script.

## 6. Testing, CI, & Documentation
- [x] Automated test suite:
  - Unit tests for configuration schema, migration, and backup (`tests/test_config.py`).
  - Safe calculator engine and AST boundary tests (`tests/test_calculator.py`).
  - File operations and path security tests (`tests/test_file_operations.py`).
  - System monitor procfs parsing and permission handling (`tests/test_system_monitor.py`).
  - Installer idempotency and rollback tests (`tests/test_installer.py`).
  - Asset metadata, desktop file, and INI syntax checks (`tests/test_desktop_assets.py`).
  - Automated ADR coverage audit (`tests/test_adr_coverage.py`).
- [x] Comprehensive documentation in `docs/`: architecture, data flow, design system, compatibility, security, troubleshooting, installation.
- [x] Complete collection of 17 Architecture Decision Records (ADRs) with 100% test-verified file coverage.
- [x] Root README.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE.
