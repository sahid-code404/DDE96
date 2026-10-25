# ADR-0013: Idempotent User/System Installer and Rollback

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
Desktop customization installers frequently suffer from critical defects:
1. They require root permissions indiscriminately, modifying core system directories and risking package manager conflicts.
2. They overwrite existing configuration files (`kwinrc`, `kdeglobals`, `plasmarc`) without taking backups, leaving users with broken sessions and no way to revert.
3. They are not idempotent: running the installer a second time creates duplicate panels, duplicate desktop entries, or broken symlinks.
4. Uninstallation is either nonexistent or destructive, accidentally wiping unrelated user configurations.

## Scope and Requirements
1. Build `desktop-installer/install.sh`:
   - Dual-mode: `--user` (default, installs into `~/.local/`, `~/.config/`, requires NO root) and `--system` (installs into `/usr/share/`, `/etc/`, requires sudo/root).
   - Strict idempotence: safe to run multiple times without duplicate side effects or broken state.
   - Automatic pre-installation snapshot: backs up existing KDE configurations (`kwinrc`, `kdeglobals`, `plasma-org.kde.plasma.desktop-appletsrc`) to `~/.config/glasswave/kde-backups/<timestamp>/`.
   - Never deletes or modifies user personal files or unrelated desktop sessions (GNOME remains untouched).
2. Build `desktop-installer/uninstall.sh`:
   - Complete removal of Glasswave-owned files, plasmoids, themes, icons, and desktop entries.
   - Clean restoration of pre-installation KDE configurations from the backup snapshot.
   - Idempotent and safe to run multiple times.
3. Build `desktop-installer/session-toggle.sh`:
   - Rapid switching between Glasswave Desktop layout and Default KDE Plasma layout without uninstalling files.

## Current Behavior / Previous Implementation
No installation or uninstallation scripts existed in the workspace.

## Decision Made
1. Implement `install.sh` and `uninstall.sh` in robust bash with `set -euo pipefail`.
2. Implement `desktop-installer/backup_manager.py` to handle programmatic backup discovery, verification, and restoration.
3. Distinguish clearly between user and system prefixes:
   - User: `XDG_DATA_HOME` (`~/.local/share`), `XDG_CONFIG_HOME` (`~/.config`), `~/.local/bin`.
   - System: `/usr/share`, `/etc/xdg`, `/usr/bin`.
4. Register uninstaller manifest in `~/.config/glasswave/installed_files.manifest` for exact, deterministic cleanup.

## Detailed Rationale
A safe, manifest-driven installer with automatic configuration snapshotting protects user systems from breakage, ensures upgrade safety, and guarantees that users can completely revert to vanilla KDE at any time.

## Alternatives Evaluated
1. **Piping curl script directly to bash (`curl | sudo bash`):** Completely prohibited by project security guidelines.
2. **Directly overwriting distro RPM files:** Prohibited; risks breaking package manager integrity.

## Architecture and Implementation Consequences
- Provides convenient CLI commands: `glasswave-install`, `glasswave-uninstall`, `glasswave-session`.
- Safe for non-root execution.

## Dependencies and Version Constraints
- Bash 4.x+, standard POSIX utilities (`cp`, `mkdir`, `rm`, `sed`).
- Python 3.10+ for backup manager.

## Security, Performance, and Accessibility
- **Security:** User mode never invokes `sudo` or modifies system files. Checks permissions before file creation.
- **Performance:** Installation finishes in <3 seconds without rebuilding heavy packages.
- **Accessibility:** Preserves any existing user accessibility settings in KDE.

## Exact List of Affected Files
- `desktop-installer/install.sh`
- `desktop-installer/uninstall.sh`
- `desktop-installer/session-toggle.sh`
- `desktop-installer/backup_manager.py`
- `docs/installation.md`
- `docs/adr/0013-installer-and-rollback-safety.md`

## Tests Created or Modified
- `tests/test_installer.py` (unit tests for installer dry-run, idempotence, manifest tracking, backup creation, and rollback)

## Build and Validation Results
Install and uninstall scripts pass syntax verification (`bash -n`) and simulated installation tests.

## Known Limitations and Unresolved Risks
If a user manually moves or deletes the backup directory in `~/.config/glasswave/kde-backups/`, the uninstaller falls back to restoring KDE's default Breeze theme.

## Rollback or Recovery Procedure
Run `desktop-installer/uninstall.sh` or `glasswave-uninstall`.

## Related ADRs
- Related to ADR-0001, ADR-0003, ADR-0012, and ADR-0014.
