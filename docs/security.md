# Glasswave Desktop Security Policy & Architecture

## 1. Core Security Guarantees
Glasswave Desktop adheres to strict Linux and Wayland security principles:
1. **Zero Silent Elevation:** No utility, installer, or application silently prompts for sudo or executes commands as root.
2. **User-Scoped Installation by Default:** Normal installation occurs entirely within `$HOME` (`~/.local/`, `~/.config/`) without touching `/usr` or `/etc`.
3. **No Unsafe Code Evaluation:** The calculator math engine parses input strictly via an Abstract Syntax Tree (AST) validator and prohibits `eval()`, `exec()`, attribute access, or unauthorized module calls.
4. **Wayland Sandbox Respect:** Screenshot and screen capture use the official FreeDesktop XDG Desktop Portal (`org.freedesktop.portal.Screenshot`) rather than bypassing compositor security.
5. **Path Traversal Protection:** File manager validates all source and destination paths, preventing arbitrary escaping outside allowed POSIX namespaces.
6. **Honest Permissions:** System monitor respects `/proc` access controls, clearly identifies user vs system processes, and reports permission boundaries honestly without faking data.
7. **No Plain-Text Secrets:** Configuration schemas forbid storing credentials or API tokens in plain text.

## 2. File Permissions & Ownership
- Configuration files: `0600` (Owner read/write only).
- Executables & Scripts: `0755` (Owner write, standard execution).
- Data files & Assets: `0644`.
