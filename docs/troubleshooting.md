# Glasswave Desktop Troubleshooting Guide

## 1. Common Issues & Solutions

### A. Window decorations do not show traffic lights
- **Cause:** KWin has not reloaded its decoration configuration.
- **Fix:** Run `qdbus org.kde.KWin /KWin reconfigure` or log out and log back in.
- **Check:** Ensure theme is set to `GlasswaveDark`:
  ```bash
  kreadconfig6 --file kwinrc --group "org.kde.kdecoration2" --key "theme"
  ```

### B. Translucent panels appear opaque or blur is disabled
- **Cause:** Compositing blur effect is disabled or GPU lacks hardware acceleration.
- **Fix:** Verify KWin blur effect status:
  ```bash
  kreadconfig6 --file kwinrc --group "Plugins" --key "blurEnabled"
  ```
  If false, enable via:
  ```bash
  kwriteconfig6 --file kwinrc --group "Plugins" --key "blurEnabled" "true"
  qdbus org.kde.KWin /KWin reconfigure
  ```
  Note: Glasswave provides an automatic high-contrast opaque fallback for low-power GPUs.

### C. Settings Center does not launch
- **Cause:** Missing Python GObject introspection packages.
- **Fix:** Ensure `python3-gobject`, `gtk4`, and `libadwaita` are installed:
  ```bash
  sudo dnf install python3-gobject gtk4 libadwaita
  ```

### D. Reverting to Vanilla KDE
- Run:
  ```bash
  ./desktop-installer/uninstall.sh
  ```
  Or directly restore KDE defaults via:
  ```bash
  lookandfeeltool -a org.kde.breezedark.desktop
  ```
