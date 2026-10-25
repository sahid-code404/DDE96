#!/usr/bin/env bash
# Glasswave Desktop - RPM Build Automation
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build/rpmbuild"

echo "=========================================================="
echo "Building Glasswave Desktop Fedora RPM Package"
echo "=========================================================="

mkdir -p "${BUILD_DIR}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

VERSION="1.0.0"
TARBALL="${BUILD_DIR}/SOURCES/glasswave-desktop-${VERSION}.tar.gz"

echo "[1/3] Generating release source tarball..."
tar --exclude-vcs \
    --exclude="build" \
    --exclude="__pycache__" \
    --transform "s,^,glasswave-desktop-${VERSION}/," \
    -czf "${TARBALL}" \
    -C "${PROJECT_ROOT}" \
    .

echo "[2/3] Staging spec file..."
cp "${SCRIPT_DIR}/glasswave-desktop.spec" "${BUILD_DIR}/SPECS/"

echo "[3/3] Executing rpmbuild..."
if command -v rpmbuild >/dev/null 2>&1; then
    rpmbuild --define "_topdir ${BUILD_DIR}" -ba "${BUILD_DIR}/SPECS/glasswave-desktop.spec"
    echo "=========================================================="
    echo "RPM Build Successful! Packages generated:"
    find "${BUILD_DIR}/RPMS" -name "*.rpm"
    echo "=========================================================="
else
    echo "Notice: 'rpmbuild' toolchain is not installed on this system."
    echo "The RPM spec file and source tarball have been staged successfully at:"
    echo "  ${BUILD_DIR}/SPECS/glasswave-desktop.spec"
    echo "  ${TARBALL}"
fi
