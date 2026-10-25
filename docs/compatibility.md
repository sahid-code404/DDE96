# Glasswave Desktop Compatibility Report

## 1. Verified Target Platform
- **Operating System:** Fedora Linux 45 (Rawhide) / Fedora 41 / Fedora 40.
- **Architecture:** `x86_64` (and `aarch64` compatible).
- **Desktop Session:** KDE Plasma 6 Wayland session (`plasma-workspace >= 6.0`, KWin 6.x).
- **Frameworks & Toolkits:**
  - KDE Frameworks 6.x (`kf6-kirigami`, `kf6-kcolorscheme`, `kf6-breeze-icons`).
  - Qt 6.6+ (`qt6-qtbase`, `qt6-qtdeclarative`, `qt6-qtsvg`).
  - GTK 4.x & Libadwaita 1.x.
  - Python 3.10+.

## 2. Tested Compatibility Matrix

| Component | Target Version | Status | Fallback Behavior |
|:---|:---|:---|:---|
| Plasma Look-and-Feel | Plasma 6.0 - 6.7+ | Verified | Breeze Look-and-Feel |
| Aurorae Window Decoration | KWin 6.0+ | Verified | Standard Breeze SSD |
| Floating Dock Plasmoid | Plasma 6.0+ | Verified | Companion Shell Runner |
| Top Bar Plasmoid | Plasma 6.0+ | Verified | Standard Plasma Panel |
| KWin Blur Effect | KWin Wayland / X11 | Verified | High-contrast opaque surfaces |
| XDG Screenshot Portal | Desktop Portal 1.16+ | Verified | KDE Spectacle direct execution |
| Global Application Menu | Qt / GTK appmenu | Verified | Standard in-window menu bar |

## 3. Coexistence with Other Desktops
- **GNOME:** Glasswave does NOT replace, conflict with, or remove GNOME Shell, GDM, or Mutter. A user can freely log into GNOME Wayland without interference.
- **Vanilla KDE Plasma:** Glasswave creates automatic backups before applying its layout. Users can return to vanilla KDE at any time via `glasswave-session --disable` or `desktop-installer/uninstall.sh`.
