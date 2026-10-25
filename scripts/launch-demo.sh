#!/usr/bin/env bash
# Glasswave Desktop - Live Demo & Companion Shell Launcher
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Launching Glasswave Desktop Companion Shell..."
python3 "${PROJECT_ROOT}/desktop-shell/companion/shell_companion.py" "$@"
