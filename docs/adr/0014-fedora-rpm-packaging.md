# ADR-0014: Fedora RPM Packaging and Dependency Model

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
For enterprise stability, reproducible deployments, and clean distribution on Fedora Linux, desktop software should be packaged as native RPM packages adhering to Fedora Packaging Guidelines.
An RPM specification file must:
1. Define clear package metadata (Name, Version, Release, License, URL, Summary, Description).
2. Explicitly declare BuildRequires and runtime Requires (Plasma workspace, Qt 6, KDE Frameworks 6, Python 3, GTK 4, Libadwaita).
3. Follow Fedora filesystem hierarchy standards (`/usr/share/plasma/`, `/usr/share/icons/`, `/usr/share/color-schemes/`, `/usr/bin/`).
4. Support standard RPM scriptlets (`%post`, `%postun`) for updating icon caches and desktop databases without breaking system integrity.
5. Provide automated build and validation scripts.

## Scope and Requirements
1. Author `desktop-packaging/glasswave-desktop.spec`:
   - Valid Fedora RPM spec file for `glasswave-desktop`.
   - Complete file listings (`%files`) covering all sub-packages (theme, shell, apps, config).
   - Scriptlets for `gtk-update-icon-cache`, `update-desktop-database`, and `kbuildsycoca6`.
2. Author build automation script `desktop-packaging/build-rpm.sh`.

## Current Behavior / Previous Implementation
No RPM spec file existed in the workspace.

## Decision Made
1. Author `desktop-packaging/glasswave-desktop.spec` with:
   - Version 1.0.0, Release 1%{?dist}.
   - Clear subpackages:
     - `glasswave-desktop-common`: Themes, icons, wallpapers, color schemes, design tokens.
     - `glasswave-desktop-shell`: Plasma 6 plasmoids, layout scripts, and companion shell.
     - `glasswave-desktop-apps`: Files, terminal, calculator, monitor, screenshot, settings.
     - `glasswave-desktop`: Meta-package pulling in all components.
   - Declared dependencies matching Fedora package names (`plasma-workspace >= 6.0`, `kf6-kirigami`, `qt6-qtbase-gui`, `python3-gobject`, `gtk4`, `libadwaita`).
2. Provide `desktop-packaging/build-rpm.sh` for local tarball generation and rpmbuild staging.

## Detailed Rationale
Modular RPM packaging allows system administrators and users to install either the entire desktop suite or individual components (e.g. just the themes or just the apps) while ensuring all system dependencies are verified by DNF.

## Alternatives Evaluated
1. **Flatpak only:** Flatpaks run sandboxed and cannot install system-wide Plasma global themes, KWin scripts, or window decorations.
2. **Raw archive distribution:** Does not resolve dependencies or provide automated update tracking through Fedora's package manager.

## Architecture and Implementation Consequences
- Provides `glasswave-desktop.spec` conforming to rpmlint standards.
- Files installed via RPM are registered in the RPM database for reliable uninstallation and upgrades.

## Dependencies and Version Constraints
- Target distribution: Fedora 40/41/42/45+.
- `rpm-build` toolchain when building packages.

## Security, Performance, and Accessibility
- **Security:** Standard RPM file permissions (`0755` for directories/executables, `0644` for data files); signed RPM releases supported.
- **Performance:** Pre-packaged assets avoid runtime compilation.
- **Accessibility:** Declares accessibility dependencies (`at-spi2-core`).

## Exact List of Affected Files
- `desktop-packaging/glasswave-desktop.spec`
- `desktop-packaging/build-rpm.sh`
- `docs/adr/0014-fedora-rpm-packaging.md`

## Tests Created or Modified
- `tests/test_desktop_assets.py` (validates spec file syntax, tags, and file macro completeness)

## Build and Validation Results
Spec file validated for correct syntax, directory ownership, scriptlet safety, and dependencies.

## Known Limitations and Unresolved Risks
Building binary RPMs on machines without `rpmbuild` installed can be done via container or mock build environments.

## Rollback or Recovery Procedure
`sudo dnf remove glasswave-desktop` or `rpm -e glasswave-desktop`.

## Related ADRs
- Related to ADR-0001, ADR-0003, and ADR-0013.
