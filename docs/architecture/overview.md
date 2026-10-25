# Glasswave Desktop - Architecture Overview

## 1. System Mission
Glasswave Desktop is an integrated, macOS-inspired desktop environment built on KDE Plasma 6 and Wayland for Fedora Linux. It delivers the visual discipline, translucency, refined typography, and smooth interaction ergonomics of modern macOS while retaining KDE Plasma's stability, multi-monitor maturity, and deep configurability.

## 2. Architectural Principles
- **Extend Rather Than Fork:** Glasswave leverages KDE Plasma 6's public extension APIs—Look-and-Feel packages, Plasma applets (plasmoids), Aurorae window decorations, KWin scripts, and FreeDesktop standards—rather than maintaining brittle forks of KWin or Plasma Shell.
- **Single Source of Truth:** Branding metadata and visual design tokens are centrally stored in `desktop-theme/branding.json` and `desktop-theme/tokens.json`.
- **Safe, Idempotent State Management:** Settings are schema-validated (`desktop-settings/schema.json`) and persisted atomically, with automatic snapshots before any migration.
- **Honest System Integration:** All system monitors, calculators, file managers, and screenshot utilities respect Linux permissions and Wayland security boundaries.

## 3. High-Level Component Diagram

```
+--------------------------------------------------------------------------+
|                            USER EXPERIENCE                               |
|   +-----------------------+     +------------------------------------+   |
|   |  Top Menu Bar Panel   |     |    Floating Bottom Dock (QML)      |   |
|   |  (Appmenu, Status)    |     |    (Magnification, Indicators)     |   |
|   +-----------------------+     +------------------------------------+   |
+--------------------------------------------------------------------------+
                                    |
+-----------------------------------+--------------------------------------+
|                     APPLICATIONS & TOOLS SUITE                           |
|  [Files]     [Terminal]     [Calculator]    [Monitor]     [Screenshot]   |
| (Finder-like)(Translucent)   (AST Safe)     (Procfs)      (XDG Portal)   |
|         \          |              |             |              /         |
|          +---------+--------------+-------------+-------------+          |
|                                   |                                      |
|                     [Control Center / Settings]                          |
|                     (Appearance, Dock, Blur, Motion)                     |
+-----------------------------------+--------------------------------------+
                                    |
+-----------------------------------+--------------------------------------+
|                       DESKTOP THEME & EFFECTS                            |
|  - Plasma Look-and-Feel (org.glasswave.desktop)                          |
|  - Aurorae Window Decorations (GlasswaveDark / GlasswaveLight)           |
|  - Frosted Plasma Style & Vector Wallpapers                              |
|  - KWin Rules & Backdrop Blur Shader Configuration                       |
|  - Cohesive Icon Theme (Glasswave Squircles)                             |
+-----------------------------------+--------------------------------------+
                                    |
+-----------------------------------+--------------------------------------+
|               SETTINGS, PACKAGING & SYSTEM FOUNDATION                    |
|  - SettingsManager (JSON Schema, Atomic Writes, Timestamped Backups)     |
|  - Installer & Rollback Manager (Idempotent User & System Modes)         |
|  - Fedora RPM Packaging (glasswave-desktop.spec)                         |
|  - KDE Plasma 6.x / KWin / Wayland / Linux Kernel 6.x+                   |
+--------------------------------------------------------------------------+
```

## 4. Component Boundaries & Responsibilities

| Component | Responsibility | Primary Technologies |
|:---|:---|:---|
| `desktop-theme` | Global look-and-feel, color schemes, Plasma style SVG surfaces, window decorations, wallpapers, tokens | KPackage, Aurorae SVG, QML, JSON |
| `desktop-icons` | Cohesive squircle icons for applications, mimetypes, and status indicators | FreeDesktop Icon Theme, SVG |
| `desktop-shell` | Dock plasmoid, Top Bar, Quick Settings popover, Launcher, Companion runner | Plasma 6 QML, Kirigami, GTK 4 |
| `desktop-effects` | KWin window rules, blur settings, overview scripts | KWin Scripting, KConfig |
| `desktop-control-center` | Glasswave Settings & Appearance Center GUI | Python 3, GTK 4, Libadwaita |
| `desktop-apps` | First-party applications (Files, Terminal, Calculator, Monitor, Screenshot) | Python 3, GTK 4, VTE, Cairo, AST |
| `desktop-settings` | Schema validation, persistence, atomic file writing, backup/rollback | JSON Schema, Python 3, CLI |
| `desktop-installer` | Non-destructive user/system installer, uninstaller, snapshot manager | POSIX Bash, Python 3 |
| `desktop-packaging` | Fedora RPM specifications and build automation | RPM Spec, rpmlint |
| `tests` | Automated unit, static, schema, asset, and ADR coverage validation | Python `unittest`, Bash |
