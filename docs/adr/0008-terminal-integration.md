# ADR-0008: Terminal Integration and Translucent Shell Styling (glasswave-terminal)

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
A premium macOS desktop requires an elegant terminal experience:
- Translucent frosted glass window background with subtle blur.
- Traffic light window controls in the top bar.
- Clean typography (Monospace / SF Mono inspired), smooth cursor blinking, and pleasant color schemes.
- Real PTY (pseudoterminal) shell execution without security compromises or silent root elevation.
- Multiple tabs, split views, clipboard copy/paste, search, and profile configuration.
- Native integration with Konsole when the user prefers standard KDE terminal workflows.

## Scope and Requirements
1. Build `glasswave-terminal` (`desktop-apps/terminal/terminal.py`):
   - macOS-inspired terminal window with translucent dark glass styling, rounded corners, and tab bar.
   - Genuine Linux pseudoterminal (`pty` / VTE or PTY subprocess) running the user's `$SHELL` (bash, zsh, fish).
   - Tabs support (`Ctrl+Shift+T`, `Ctrl+Shift+W`, `Ctrl+PageUp/Down`).
   - Configurable font, font size, and background opacity via Glasswave settings.
   - Text search (`Ctrl+Shift+F`) and copy/paste (`Ctrl+Shift+C`, `Ctrl+Shift+V`).
2. Provide pre-configured Glasswave color scheme and profile for KDE Konsole (`Glasswave.colorscheme` and `Glasswave.profile`).

## Current Behavior / Previous Implementation
No custom Glasswave terminal emulator existed. Konsole was installed with default Breeze theme.

## Decision Made
1. Develop `glasswave-terminal` leveraging Python 3 and VTE (via `gi.repository.Vte` when present or robust POSIX PTY/subprocess wrapper) styled with custom Glasswave frosted glass CSS.
2. Provide Konsole integration assets (`desktop-apps/terminal/Glasswave.colorscheme`) so KDE users who prefer Konsole can automatically use the matching Glasswave theme.
3. Install desktop launcher `org.glasswave.terminal.desktop` registered for terminal execution.

## Detailed Rationale
This hybrid approach guarantees that users receive a macOS-style terminal with authentic window chrome and translucency, while also styling KDE's native Konsole for power users.

## Alternatives Evaluated
1. **Writing a terminal emulator from scratch without PTY:** Completely unacceptable; terminal must support ANSI/VT100 escape codes, termios, ncurses, and interactive programs (vim, htop).
2. **Wrapping Alacritty / Kitty directly:** Adds external dependencies that are not standard in Fedora Plasma base installations.

## Architecture and Implementation Consequences
- Provides `glasswave-terminal` executable and desktop entry.
- Safe execution: runs commands as the unprivileged logged-in user without hidden sudo or privileged helpers.

## Dependencies and Version Constraints
- Python 3.10+
- `gi.repository.Gtk` (4.0 or 3.0) or POSIX terminal integration.

## Security, Performance, and Accessibility
- **Security:** Never elevates privileges or executes commands without user input.
- **Performance:** Hardware-accelerated glyph rendering via Pango/Cairo.
- **Accessibility:** High text contrast guarantees readability regardless of background wallpaper.

## Exact List of Affected Files
- `desktop-apps/terminal/__init__.py`
- `desktop-apps/terminal/terminal.py`
- `desktop-apps/terminal/Glasswave.colorscheme`
- `desktop-apps/terminal/org.glasswave.terminal.desktop`
- `docs/adr/0008-terminal-integration.md`

## Tests Created or Modified
- `tests/test_desktop_assets.py` (validates Konsole color scheme syntax and desktop entry)
- PTY allocation and shell environment smoke tests

## Build and Validation Results
Terminal launches cleanly, allocates PTY, executes standard shell commands, and handles tab switching.

## Known Limitations and Unresolved Risks
Backdrop blur for the terminal window requires KWin compositor blur effect to be active.

## Rollback or Recovery Procedure
Revert default terminal to Konsole via `xdg-mime default org.kde.konsole.desktop`.

## Related ADRs
- Related to ADR-0001, ADR-0002, and ADR-0005.
