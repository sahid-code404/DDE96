# Glasswave Desktop

> A complete, premium, macOS-inspired Linux desktop experience built on KDE Plasma 6 and Wayland.

Glasswave Desktop combines the visual refinement, translucent frosted glass materials, fluid animations, elegant typography, and cohesive application suite associated with modern macOS with the flexibility, stability, and open architecture of Linux and KDE Plasma.

---

## Highlights

- **Refined Desktop Composition:**
  - Slim, translucent top menu bar with global menu, active window title, and system status indicators.
  - Floating bottom dock with pointer magnification, running application dots, active application bounce, and pinned launchers.
  - Traffic-light window controls (`Close`, `Minimize`, `Maximize`) positioned on the top-left with Aurorae themes.
  - Backdrop blur and frosted glass surfaces with automatic high-contrast opaque fallbacks.
- **Integrated Applications Suite:**
  - **Finder-Inspired File Manager (`glasswave-files`):** Curated sidebar, breadcrumb path bar, list/grid views, search filtering, spacebar Quick Look preview, and safe FreeDesktop trash integration.
  - **Translucent Terminal (`glasswave-terminal`):** Frosted glass styling, tabs, search, and native Konsole profile integration.
  - **Safe Calculator (`glasswave-calculator`):** macOS-style circular button UI, AST-based safe evaluation engine (zero `eval()`), and calculation history.
  - **Activity System Monitor (`glasswave-monitor`):** Real-time CPU, Memory, Disk, and Process monitoring with honest POSIX permissions.
  - **Screenshot Utility (`glasswave-screenshot`):** Floating pill HUD with full-screen, window, and region capture via the FreeDesktop XDG Desktop Portal.
- **Glasswave Control Center (`glasswave-settings`):**
  - Centralized management of Appearance, Dock, Top Bar, Window Decorations, Blur, and Reduced Motion.
  - Atomic configuration persistence with JSON schema validation.
  - Instant backup, export, import, and reset to defaults.
- **Enterprise-Grade Engineering:**
  - **Safe & Non-Destructive:** Does not replace GNOME or modify vanilla KDE files. Automatic backup of existing KDE configs before installation.
  - **Strict ADR Traceability:** Every change is governed by an Architecture Decision Record in `docs/adr/`.
  - **Comprehensive Automated Tests:** 100% test passing across configuration, security, file operations, procfs parsing, and packaging.
  - **Native Packaging:** Fedora RPM spec file (`glasswave-desktop.spec`) and idempotent installer.

---

## Quick Start

### 1. User Installation (No root needed)

```bash
git clone https://github.com/glasswave-desktop/glasswave-desktop.git
cd glasswave-desktop
./desktop-installer/install.sh --user
```

### 2. Live Preview / Companion Shell

To test and visually preview the Glasswave dock, top bar, and applications on any Wayland/X11 session:

```bash
./scripts/launch-demo.sh
```

### 3. Run Automated Tests

```bash
./scripts/run-tests.sh
```

### 4. Safe Rollback

To uninstall and restore your exact previous KDE configuration:

```bash
./desktop-installer/uninstall.sh
```

---

## Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [Data Flow](docs/architecture/data-flow.md)
- [Design System & Tokens](docs/design/design-system.md)
- [Interaction Guidelines](docs/design/interaction-guidelines.md)
- [Architecture Decision Records (ADRs)](docs/adr/README.md)
- [Compatibility Matrix](docs/compatibility.md)
- [Security Policy](docs/security.md)
- [Installation & Rollback](docs/installation.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## License

Glasswave Desktop is released under the [MIT License](LICENSE).
