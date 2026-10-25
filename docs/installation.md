# Glasswave Desktop Installation & Rollback Guide

## 1. Quick Installation (User Mode - Recommended)

User mode installs Glasswave entirely into your user directory (`~/.local/` and `~/.config/`). It requires NO root privileges and leaves all system packages untouched.

```bash
# Clone the repository
git clone https://github.com/glasswave-desktop/glasswave-desktop.git
cd glasswave-desktop

# Run the installer
./desktop-installer/install.sh --user
```

The installer will:
1. Create a timestamped backup of your current KDE Plasma configuration in `~/.config/glasswave/kde-backups/<timestamp>/`.
2. Install themes, icons, wallpapers, plasmoids, and applications into `~/.local/share/` and `~/.local/bin/`.
3. Apply the Glasswave look-and-feel and layout.

## 2. System-Wide Installation (Requires sudo)

For system administrators deploying Glasswave across all users:
```bash
sudo ./desktop-installer/install.sh --system
```
Or build and install the RPM:
```bash
./desktop-packaging/build-rpm.sh
sudo dnf install ./build/RPMS/x86_64/glasswave-desktop-*.rpm
```

## 3. Session Switching & Reversibility

To temporarily switch back to vanilla KDE without uninstalling files:
```bash
glasswave-session --disable
```
To re-enable Glasswave:
```bash
glasswave-session --enable
```

## 4. Complete Uninstallation & Rollback

To completely remove Glasswave and restore your original KDE Plasma settings:
```bash
./desktop-installer/uninstall.sh
```
The uninstaller will:
1. Restore your backed-up KDE configuration files (`kwinrc`, `kdeglobals`, `plasmarc`, etc.).
2. Delete only files registered in the Glasswave installation manifest.
3. Clean desktop and icon caches.
