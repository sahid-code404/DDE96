#!/usr/bin/env bash
# Glasswave Desktop - Idempotent Installer
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

MODE="user"
DRY_RUN=0

for arg in "$@"; do
    case "$arg" in
        --user)
            MODE="user"
            ;;
        --system)
            MODE="system"
            ;;
        --dry-run)
            DRY_RUN=1
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: $0 [--user|--system] [--dry-run]"
            exit 1
            ;;
    esac
done

if [[ "$MODE" == "system" && "$EUID" -ne 0 ]]; then
    echo "Error: System-wide installation requires root privileges (sudo)." >&2
    exit 1
fi

if [[ "$MODE" == "user" ]]; then
    PREFIX="${HOME}/.local"
    CONFIG_DIR="${XDG_CONFIG_HOME:-${HOME}/.config}"
    DATA_DIR="${PREFIX}/share"
    BIN_DIR="${PREFIX}/bin"
else
    PREFIX="/usr"
    CONFIG_DIR="/etc/xdg"
    DATA_DIR="${PREFIX}/share"
    BIN_DIR="${PREFIX}/bin"
fi

echo "=========================================================="
echo "Installing Glasswave Desktop [Mode: ${MODE}]"
echo "Prefix: ${PREFIX}"
echo "=========================================================="

# 1. Snapshot existing KDE configurations (in user mode)
if [[ "$MODE" == "user" && "$DRY_RUN" -eq 0 ]]; then
    echo "[1/5] Creating pre-installation KDE configuration snapshot..."
    python3 "${SCRIPT_DIR}/backup_manager.py" backup
else
    echo "[1/5] Skipping KDE snapshot (system mode or dry-run)"
fi

# 2. Prepare directories
MANIFEST_DIR="${HOME}/.config/glasswave"
MANIFEST_FILE="${MANIFEST_DIR}/installed_files.manifest"
if [[ "$DRY_RUN" -eq 0 ]]; then
    mkdir -p "${MANIFEST_DIR}"
    mkdir -p "${BIN_DIR}"
    mkdir -p "${DATA_DIR}/color-schemes"
    mkdir -p "${DATA_DIR}/plasma/look-and-feel"
    mkdir -p "${DATA_DIR}/plasma/desktoptheme"
    mkdir -p "${DATA_DIR}/aurorae/themes"
    mkdir -p "${DATA_DIR}/wallpapers/Glasswave"
    mkdir -p "${DATA_DIR}/icons"
    mkdir -p "${DATA_DIR}/plasma/plasmoids"
    mkdir -p "${DATA_DIR}/applications"
    : > "${MANIFEST_FILE}" # clear/init manifest
fi

track_file() {
    local target="$1"
    if [[ "$DRY_RUN" -eq 0 ]]; then
        echo "$target" >> "${MANIFEST_FILE}"
    fi
}

copy_asset() {
    local src="$1"
    local dst="$2"
    echo "  -> Copying ${src} to ${dst}"
    if [[ "$DRY_RUN" -eq 0 ]]; then
        cp -r "${src}" "${dst}"
        track_file "${dst}"
    fi
}

echo "[2/5] Deploying Themes, Wallpapers, and Icons..."
copy_asset "${PROJECT_ROOT}/desktop-theme/color-schemes/GlasswaveDark.colors" "${DATA_DIR}/color-schemes/GlasswaveDark.colors"
copy_asset "${PROJECT_ROOT}/desktop-theme/color-schemes/GlasswaveLight.colors" "${DATA_DIR}/color-schemes/GlasswaveLight.colors"
copy_asset "${PROJECT_ROOT}/desktop-theme/plasma-look-and-feel/org.glasswave.desktop" "${DATA_DIR}/plasma/look-and-feel/"
copy_asset "${PROJECT_ROOT}/desktop-theme/plasma-style/org.glasswave.desktop" "${DATA_DIR}/plasma/desktoptheme/"
copy_asset "${PROJECT_ROOT}/desktop-theme/aurorae/GlasswaveDark" "${DATA_DIR}/aurorae/themes/"
copy_asset "${PROJECT_ROOT}/desktop-theme/aurorae/GlasswaveLight" "${DATA_DIR}/aurorae/themes/"
copy_asset "${PROJECT_ROOT}/desktop-theme/wallpapers/" "${DATA_DIR}/wallpapers/Glasswave"
copy_asset "${PROJECT_ROOT}/desktop-icons/Glasswave" "${DATA_DIR}/icons/"

echo "[3/5] Deploying Plasma 6 Shell Plasmoids..."
copy_asset "${PROJECT_ROOT}/desktop-shell/plasmoids/org.glasswave.dock" "${DATA_DIR}/plasma/plasmoids/"
copy_asset "${PROJECT_ROOT}/desktop-shell/plasmoids/org.glasswave.topbar" "${DATA_DIR}/plasma/plasmoids/"
copy_asset "${PROJECT_ROOT}/desktop-shell/plasmoids/org.glasswave.quicksettings" "${DATA_DIR}/plasma/plasmoids/"
copy_asset "${PROJECT_ROOT}/desktop-shell/plasmoids/org.glasswave.launcher" "${DATA_DIR}/plasma/plasmoids/"

echo "[4/5] Deploying Application Binaries and Desktop Entries..."
install_bin() {
    local src="$1"
    local name="$2"
    local dst="${BIN_DIR}/${name}"
    echo "  -> Installing executable ${name}"
    if [[ "$DRY_RUN" -eq 0 ]]; then
        cp "${src}" "${dst}"
        chmod 755 "${dst}"
        track_file "${dst}"
    fi
}

install_bin "${PROJECT_ROOT}/desktop-control-center/control_center.py" "glasswave-settings"
install_bin "${PROJECT_ROOT}/desktop-apps/files/file_manager.py" "glasswave-files"
install_bin "${PROJECT_ROOT}/desktop-apps/terminal/terminal.py" "glasswave-terminal"
install_bin "${PROJECT_ROOT}/desktop-apps/calculator/calculator_ui.py" "glasswave-calculator"
install_bin "${PROJECT_ROOT}/desktop-apps/monitor/monitor_ui.py" "glasswave-monitor"
install_bin "${PROJECT_ROOT}/desktop-apps/screenshot/screenshot.py" "glasswave-screenshot"
install_bin "${PROJECT_ROOT}/desktop-settings/cli.py" "glasswave-config"
install_bin "${PROJECT_ROOT}/desktop-shell/companion/shell_companion.py" "glasswave-shell-companion"
install_bin "${PROJECT_ROOT}/desktop-installer/session-toggle.sh" "glasswave-session"

copy_asset "${PROJECT_ROOT}/desktop-control-center/org.glasswave.settings.desktop" "${DATA_DIR}/applications/"
copy_asset "${PROJECT_ROOT}/desktop-apps/files/org.glasswave.files.desktop" "${DATA_DIR}/applications/"
copy_asset "${PROJECT_ROOT}/desktop-apps/terminal/org.glasswave.terminal.desktop" "${DATA_DIR}/applications/"
copy_asset "${PROJECT_ROOT}/desktop-apps/calculator/org.glasswave.calculator.desktop" "${DATA_DIR}/applications/"
copy_asset "${PROJECT_ROOT}/desktop-apps/monitor/org.glasswave.monitor.desktop" "${DATA_DIR}/applications/"
copy_asset "${PROJECT_ROOT}/desktop-apps/screenshot/org.glasswave.screenshot.desktop" "${DATA_DIR}/applications/"

echo "[5/5] Initializing Configuration and Applying Layout..."
if [[ "$DRY_RUN" -eq 0 ]]; then
    python3 "${PROJECT_ROOT}/desktop-settings/cli.py" validate >/dev/null 2>&1 || true

    # If KDE commands are available, apply theme
    if command -v lookandfeeltool >/dev/null 2>&1; then
        echo "  -> Applying Glasswave look-and-feel via lookandfeeltool..."
        lookandfeeltool -a org.glasswave.desktop || true
    fi
    if command -v kbuildsycoca6 >/dev/null 2>&1; then
        kbuildsycoca6 --noincremental >/dev/null 2>&1 || true
    fi
fi

echo "=========================================================="
echo "Glasswave Desktop installation completed successfully!"
echo "To switch layouts at any time, run: glasswave-session"
echo "To rollback and uninstall, run: ${SCRIPT_DIR}/uninstall.sh"
echo "=========================================================="
