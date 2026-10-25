# Glasswave Desktop - Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records (ADRs) for the Glasswave Desktop project.
In accordance with the project policy, **every implementation change is documented in an ADR**.

## ADR Index

| ADR ID | Title | Status | Primary Component | Tests & Verification |
|:---|:---|:---|:---|:---|
| [ADR-0001](0001-project-architecture.md) | Glasswave Desktop Architecture & KDE Extension Model | Accepted | Core Architecture | Static Architecture Verification |
| [ADR-0002](0002-design-system-and-tokens.md) | Centralized Design System, Tokens, and Materials | Accepted | desktop-theme | Asset & Token Validation |
| [ADR-0003](0003-plasma-theme-and-color-schemes.md) | Plasma 6 Look-and-Feel, Styles, and Color Schemes | Accepted | desktop-theme | Color Scheme & Plasma INI Tests |
| [ADR-0004](0004-dock-and-topbar-architecture.md) | Floating Dock and Top Bar Shell Architecture | Accepted | desktop-shell | Applet Metadata & Shell Tests |
| [ADR-0005](0005-kwin-effects-and-window-decorations.md) | KWin Window Decorations, Blur, and Effects Rules | Accepted | desktop-effects | Decoration & Config Checks |
| [ADR-0006](0006-settings-and-control-center.md) | Glasswave Settings and Appearance Center | Accepted | desktop-control-center | Settings Backend & UI Unit Tests |
| [ADR-0007](0007-finder-file-manager.md) | Finder-Inspired File Management Architecture | Accepted | desktop-apps/files | File Operations & Security Tests |
| [ADR-0008](0008-terminal-integration.md) | Terminal Integration and Translucent Shell Styling | Accepted | desktop-apps/terminal | Terminal Launch & Config Checks |
| [ADR-0009](0009-calculator-engine-and-ast.md) | Calculator Math Engine with Safe AST Parser | Accepted | desktop-apps/calculator | Calculator Engine & Precision Tests |
| [ADR-0010](0010-system-monitor-and-permissions.md) | System Monitor Architecture and Honest Permissions | Accepted | desktop-apps/monitor | Procfs Parsing & Bound Tests |
| [ADR-0011](0011-screenshot-and-portals.md) | Wayland Screenshot Utility via XDG Desktop Portal | Accepted | desktop-apps/screenshot | Portal Detection & CLI Checks |
| [ADR-0012](0012-configuration-schema-and-migration.md) | Central Configuration Schema, Backup, and Reset | Accepted | desktop-settings | Schema Validation & Migration Tests |
| [ADR-0013](0013-installer-and-rollback-safety.md) | Idempotent User/System Installer and Rollback | Accepted | desktop-installer | Install, Backup, & Rollback Tests |
| [ADR-0014](0014-fedora-rpm-packaging.md) | Fedora RPM Packaging and Dependency Model | Accepted | desktop-packaging | RPM Spec Linting & Packaging Checks |
| [ADR-0015](0015-automated-test-suite-and-ci.md) | Automated Test Suite and ADR Coverage Validation | Accepted | tests | Automated Test Suite Run |
| [ADR-0016](0016-aurorae-light-decorations-and-status-icons.md) | Aurorae Light Window Decoration Button Assets and Symbolic Status Icons | Accepted | desktop-theme / desktop-icons | SVG Well-Formedness & Asset Tests |
| [ADR-0017](0017-kde-system-settings-synchronization.md) | KDE System Settings Synchronization, Module Resolution, and Asset Integration | Accepted | desktop-settings / desktop-control-center | Settings Sync & Module Resolution Tests |
| [ADR-0018](0018-pygobject-vfunc-chaining-and-activation-order-fix.md) | PyGObject Virtual Method Chaining and Control Center Activation Order Fix | Accepted | desktop-apps / desktop-control-center | Process Startup & Rendering Tests |

## ADR Lifecycle and Rules

1. **Mandatory Documentation:** No implementation file may be added or modified without being tracked in at least one corresponding ADR.
2. **Automated Verification:** The project test suite includes `test_adr_coverage.py` which inspects all non-generated implementation files and validates mapping to an accepted ADR.
3. **Immutability:** Accepted ADRs are historical records; architectural modifications are recorded via superseding ADRs.
