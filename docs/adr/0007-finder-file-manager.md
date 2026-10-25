# ADR-0007: Finder-Inspired File Manager (glasswave-files)

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
A hallmark of macOS is Finder: a clean, uncluttered, multi-view file manager with a curated sidebar of standard locations, breadcrumb navigation, quick search filtering, spacebar Quick Look preview, and safe file operations (including trash integration and undo).
Existing Linux file managers (e.g. Dolphin or Nautilus) either have complex multi-toolbar layouts that clash with the macOS aesthetic or lack specific macOS interaction ergonomics.

## Scope and Requirements
1. Build `glasswave-files` (`desktop-apps/files/file_manager.py`) with:
   - macOS-inspired window design with traffic-light window controls, integrated header search bar, and view switcher (Icons / List).
   - Curated sidebar: Favorites (Home, Desktop, Documents, Downloads, Music, Pictures, Videos, Trash), Devices, and Bookmarks.
   - Interactive breadcrumb navigation bar + path entry mode (`Ctrl+L`).
   - File viewing: List view (with sortable columns: Name, Size, Date Modified, Kind) and Grid icon view.
   - Core file operations: Create Folder, Rename, Copy, Cut, Paste, Delete, Move to Trash, Restore from Trash.
   - Multi-selection support (Shift+Click, Ctrl+Click, rubberband drag selection).
   - Spacebar Quick Look / preview overlay for images, text, and documents.
   - Open-with integration using standard XDG desktop applications.
   - Hidden files toggle (`Ctrl+H`).
2. Integrate with KDE's Dolphin when users choose standard Dolphin workflows.

## Current Behavior / Previous Implementation
No custom macOS-inspired file manager existed for Glasswave.

## Decision Made
1. Develop `glasswave-files` using Python 3 and GTK 4 / Libadwaita with custom Glasswave frosted CSS theme.
2. Implement file system operations via standard Python `pathlib`, `shutil`, `os`, and FreeDesktop Trash specification (`~/.local/share/Trash`).
3. Ensure strict path traversal validation: all operations validate destination paths, check permissions, and confirm destructive permanent deletions.
4. Provide desktop launcher `org.glasswave.files.desktop` registered as an XDG file manager handler.

## Detailed Rationale
Developing a dedicated Finder-inspired application gives the user the authentic macOS file management experience with instant responsiveness, modern typography, and clean layouts, while maintaining standard Linux filesystem permissions and FreeDesktop trash compliance.

## Alternatives Evaluated
1. **Theming Dolphin exclusively:** Dolphin's C++ codebase hardcodes many layout conventions (status bar, multi-dock panels, URL navigator) that cannot be altered into a clean macOS Finder layout via stylesheets alone.
2. **Nautilus wrapper:** Nautilus is tightly coupled to GNOME Shell and lacks fine-grained KDE integration and custom Glasswave token support.

## Architecture and Implementation Consequences
- The application can be launched via `glasswave-files` or through the desktop launcher.
- Seamlessly interoperates with Dolphin: Dolphin remains installed and accessible as an alternative or power-user tool.

## Dependencies and Version Constraints
- Python 3.10+
- `gi.repository.Gtk` (4.0)
- `gi.repository.Gio` (2.0)
- `gi.repository.GLib` (2.0)

## Security, Performance, and Accessibility
- **Security:** Strict permission checking before modifying files; trash integration avoids accidental permanent data loss; paths are canonicalized against directory traversal attacks.
- **Performance:** Directory listings are loaded efficiently; thumbnail rendering uses cached pixbufs.
- **Accessibility:** Full keyboard traversal (arrows, Return, spacebar, Ctrl+C, Ctrl+V, Delete).

## Exact List of Affected Files
- `desktop-apps/files/__init__.py`
- `desktop-apps/files/file_manager.py`
- `desktop-apps/files/org.glasswave.files.desktop`
- `docs/adr/0007-finder-file-manager.md`

## Tests Created or Modified
- `tests/test_file_operations.py` (validates path safety, trash move/restore, directory listing, copy/cut/paste mechanics)

## Build and Validation Results
All automated file operation tests passed; path traversal protections verified.

## Known Limitations and Unresolved Risks
Network browsing (e.g. SMB / WebDAV shares) relies on underlying GIO/GVFS or KIO mounts.

## Rollback or Recovery Procedure
Revert default file manager to Dolphin via `xdg-mime default org.kde.dolphin.desktop inode/directory`.

## Related ADRs
- Related to ADR-0001, ADR-0002, and ADR-0012.
