#!/usr/bin/env bash
# Glasswave Desktop - Automated Test Suite Runner
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=========================================================="
echo "Running Glasswave Desktop Automated Test Suite"
echo "Root: ${PROJECT_ROOT}"
echo "=========================================================="

cd "${PROJECT_ROOT}"

# Run Python Unit & Static Tests
python3 -m unittest discover -s tests -v

echo "=========================================================="
echo "All tests passed successfully!"
echo "=========================================================="
