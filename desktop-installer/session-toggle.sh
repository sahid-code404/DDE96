#!/usr/bin/env bash
# Glasswave Desktop - Session Toggle Utility
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_usage() {
    echo "Usage: glasswave-session [--enable|--disable|--status]"
    echo "  --enable   Apply Glasswave macOS-inspired theme and layout"
    echo "  --disable  Revert to standard default KDE Plasma theme and layout"
    echo "  --status   Show current active session theme"
}

if [[ $# -eq 0 ]]; then
    show_usage
    exit 0
fi

ACTION="$1"
case "$ACTION" in
    --enable)
        echo "Enabling Glasswave Desktop session..."
        if command -v lookandfeeltool >/dev/null 2>&1; then
            lookandfeeltool -a org.glasswave.desktop
        fi
        if command -v qdbus >/dev/null 2>&1; then
            qdbus org.kde.KWin /KWin reconfigure 2>/dev/null || true
        fi
        echo "Glasswave Desktop enabled."
        ;;
    --disable)
        echo "Disabling Glasswave Desktop and reverting to default KDE session..."
        if command -v lookandfeeltool >/dev/null 2>&1; then
            lookandfeeltool -a org.kde.breezedark.desktop
        fi
        if command -v qdbus >/dev/null 2>&1; then
            qdbus org.kde.KWin /KWin reconfigure 2>/dev/null || true
        fi
        echo "Default KDE session restored."
        ;;
    --status)
        if command -v kreadconfig6 >/dev/null 2>&1; then
            CURRENT=$(kreadconfig6 --file kdeglobals --group KDE --key lookAndFeelPackage)
            echo "Current Look-and-Feel: ${CURRENT:-org.kde.breezedark.desktop}"
        else
            echo "KDE configuration tool not in path."
        fi
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
