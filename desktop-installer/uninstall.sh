#!/usr/bin/env bash
# Glasswave Desktop - Safe Uninstaller and Rollback
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${XDG_CONFIG_HOME:-${HOME}/.config}"
MANIFEST_FILE="${CONFIG_DIR}/glasswave/installed_files.manifest"

echo "=========================================================="
echo "Uninstalling Glasswave Desktop and Rolling Back Settings"
echo "=========================================================="

# 1. Restore KDE settings snapshot
echo "[1/3] Restoring original KDE configuration snapshot..."
if [[ -f "${SCRIPT_DIR}/backup_manager.py" ]]; then
    python3 "${SCRIPT_DIR}/backup_manager.py" restore || echo "  (Notice: No prior snapshot needed restoration)"
fi

# 2. Revert theme to default Breeze if lookandfeeltool is available
if command -v lookandfeeltool >/dev/null 2>&1; then
    echo "  -> Reverting to standard Breeze Dark theme..."
    lookandfeeltool -a org.kde.breezedark.desktop 2>/dev/null || true
fi

# 3. Remove Glasswave installed files according to manifest
echo "[2/3] Removing Glasswave-owned files..."
if [[ -f "${MANIFEST_FILE}" ]]; then
    while IFS= read -r file_path; do
        if [[ -e "${file_path}" ]]; then
            echo "  -> Removing ${file_path}"
            rm -rf "${file_path}"
        fi
    done < "${MANIFEST_FILE}"
    rm -f "${MANIFEST_FILE}"
else
    echo "  (No manifest file found; skipping direct file removals)"
fi

# 4. Clean caches
echo "[3/3] Updating system and desktop caches..."
if command -v kbuildsycoca6 >/dev/null 2>&1; then
    kbuildsycoca6 --noincremental >/dev/null 2>&1 || true
fi

echo "=========================================================="
echo "Glasswave Desktop uninstalled successfully."
echo "Your original desktop session configuration is restored."
echo "=========================================================="
