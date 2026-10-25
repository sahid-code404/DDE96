# Building Glasswave Desktop

## 1. Prerequisites
Glasswave Desktop is developed for Fedora Linux with KDE Plasma 6 Wayland session.

Standard build tools:
- `gcc` and `g++` (GCC 14+ or Clang 18+)
- `cmake` (3.25+)
- `python3` (3.10+) with `python3-gobject`
- `gtk4` and `libadwaita`
- `cairo` and `pango`
- `wayland-client` and `wayland-devel`
- `kf6-kirigami`, `plasma-workspace`, and `qt6-qtbase`

## 2. Build Commands

```bash
# Clone the repository
git clone https://github.com/glasswave-desktop/glasswave-desktop.git
cd glasswave-desktop

# Run the test suite
make test
# Or directly via script:
./scripts/run-tests.sh

# Build CMake targets
mkdir -p build && cd build
cmake ..
make -j$(nproc)

# Run demo companion shell (live preview on Wayland/X11)
./scripts/launch-demo.sh
```

## 3. Package Generation (Fedora RPM)

```bash
# Build binary and source RPMs
./desktop-packaging/build-rpm.sh
```
