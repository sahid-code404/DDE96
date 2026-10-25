cmake_minimum_required(VERSION 3.20)
project(glasswave-desktop VERSION 1.0.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(GNUInstallDirs)

# Options
option(BUILD_TESTING "Build the testing tree" ON)

message(STATUS "Configuring Glasswave Desktop v${PROJECT_VERSION}")
message(STATUS "Install prefix: ${CMAKE_INSTALL_PREFIX}")

# Install Theme Assets
install(DIRECTORY desktop-theme/color-schemes/
        DESTINATION ${CMAKE_INSTALL_DATADIR}/color-schemes
        FILES_MATCHING PATTERN "*.colors")

install(DIRECTORY desktop-theme/plasma-look-and-feel/org.glasswave.desktop
        DESTINATION ${CMAKE_INSTALL_DATADIR}/plasma/look-and-feel)

install(DIRECTORY desktop-theme/plasma-style/org.glasswave.desktop
        DESTINATION ${CMAKE_INSTALL_DATADIR}/plasma/desktoptheme)

install(DIRECTORY desktop-theme/aurorae/GlasswaveDark
        DESTINATION ${CMAKE_INSTALL_DATADIR}/aurorae/themes)

install(DIRECTORY desktop-theme/aurorae/GlasswaveLight
        DESTINATION ${CMAKE_INSTALL_DATADIR}/aurorae/themes)

install(DIRECTORY desktop-theme/wallpapers/
        DESTINATION ${CMAKE_INSTALL_DATADIR}/wallpapers/Glasswave)

# Install Icons
install(DIRECTORY desktop-icons/Glasswave
        DESTINATION ${CMAKE_INSTALL_DATADIR}/icons)

# Install Plasmoids
install(DIRECTORY desktop-shell/plasmoids/org.glasswave.dock
        DESTINATION ${CMAKE_INSTALL_DATADIR}/plasma/plasmoids)

install(DIRECTORY desktop-shell/plasmoids/org.glasswave.topbar
        DESTINATION ${CMAKE_INSTALL_DATADIR}/plasma/plasmoids)

install(DIRECTORY desktop-shell/plasmoids/org.glasswave.quicksettings
        DESTINATION ${CMAKE_INSTALL_DATADIR}/plasma/plasmoids)

install(DIRECTORY desktop-shell/plasmoids/org.glasswave.launcher
        DESTINATION ${CMAKE_INSTALL_DATADIR}/plasma/plasmoids)

# Install Desktop Applications & Utilities
install(PROGRAMS
        desktop-control-center/control_center.py
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        RENAME glasswave-settings)

install(PROGRAMS
        desktop-apps/files/file_manager.py
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        RENAME glasswave-files)

install(PROGRAMS
        desktop-apps/terminal/terminal.py
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        RENAME glasswave-terminal)

install(PROGRAMS
        desktop-apps/calculator/calculator_ui.py
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        RENAME glasswave-calculator)

install(PROGRAMS
        desktop-apps/monitor/monitor_ui.py
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        RENAME glasswave-monitor)

install(PROGRAMS
        desktop-apps/screenshot/screenshot.py
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        RENAME glasswave-screenshot)

install(PROGRAMS
        desktop-settings/cli.py
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        RENAME glasswave-config)

# Install Desktop Entries
install(FILES
        desktop-control-center/org.glasswave.settings.desktop
        desktop-apps/files/org.glasswave.files.desktop
        desktop-apps/terminal/org.glasswave.terminal.desktop
        desktop-apps/calculator/org.glasswave.calculator.desktop
        desktop-apps/monitor/org.glasswave.monitor.desktop
        desktop-apps/screenshot/org.glasswave.screenshot.desktop
        DESTINATION ${CMAKE_INSTALL_DATADIR}/applications)

# Tests target
if(BUILD_TESTING)
    enable_testing()
    add_test(NAME glasswave_suite
             COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/scripts/run-tests.sh)
endif()
