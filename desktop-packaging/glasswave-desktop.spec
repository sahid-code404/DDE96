Name:           glasswave-desktop
Version:        1.0.0
Release:        1%{?dist}
Summary:        Complete macOS-inspired desktop experience for KDE Plasma 6 Wayland

License:        MIT
URL:            https://github.com/glasswave-desktop/glasswave-desktop
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  cmake >= 3.20
BuildRequires:  python3-devel

Requires:       plasma-workspace >= 6.0
Requires:       kf6-kirigami >= 6.0
Requires:       kf6-kcolorscheme >= 6.0
Requires:       qt6-qtbase-gui >= 6.6
Requires:       qt6-qtdeclarative >= 6.6
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita

Recommends:     spectacle
Recommends:     konsole

%description
Glasswave Desktop is a premium, macOS-inspired Linux desktop experience built
on KDE Plasma 6 and Wayland for Fedora Linux. It combines the visual discipline,
translucent frosted glass materials, fluid animations, and elegant typography of
macOS with KDE Plasma's stability, configuration capabilities, and performance.

%prep
%autosetup

%build
%cmake
%cmake_build

%install
%cmake_install

%post
/bin/touch --no-create %{_datadir}/icons/Glasswave &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/Glasswave &>/dev/null || :
fi
if [ -x %{_bindir}/update-desktop-database ]; then
  %{_bindir}/update-desktop-database %{_datadir}/applications &>/dev/null || :
fi
if [ -x %{_bindir}/kbuildsycoca6 ]; then
  %{_bindir}/kbuildsycoca6 --noincremental &>/dev/null || :
fi

%postun
if [ $1 -eq 0 ]; then
  /bin/touch --no-create %{_datadir}/icons/Glasswave &>/dev/null || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/Glasswave &>/dev/null || :
  fi
  if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database %{_datadir}/applications &>/dev/null || :
  fi
  if [ -x %{_bindir}/kbuildsycoca6 ]; then
    %{_bindir}/kbuildsycoca6 --noincremental &>/dev/null || :
  fi
fi

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/glasswave-settings
%{_bindir}/glasswave-files
%{_bindir}/glasswave-terminal
%{_bindir}/glasswave-calculator
%{_bindir}/glasswave-monitor
%{_bindir}/glasswave-screenshot
%{_bindir}/glasswave-config
%{_datadir}/color-schemes/GlasswaveDark.colors
%{_datadir}/color-schemes/GlasswaveLight.colors
%{_datadir}/plasma/look-and-feel/org.glasswave.desktop/
%{_datadir}/plasma/desktoptheme/org.glasswave.desktop/
%{_datadir}/aurorae/themes/GlasswaveDark/
%{_datadir}/aurorae/themes/GlasswaveLight/
%{_datadir}/wallpapers/Glasswave/
%{_datadir}/icons/Glasswave/
%{_datadir}/plasma/plasmoids/org.glasswave.dock/
%{_datadir}/plasma/plasmoids/org.glasswave.topbar/
%{_datadir}/plasma/plasmoids/org.glasswave.quicksettings/
%{_datadir}/plasma/plasmoids/org.glasswave.launcher/
%{_datadir}/applications/org.glasswave.*.desktop

%changelog
* Sun Oct 26 2026 Glasswave Desktop Team <architect@glasswave.desktop> - 1.0.0-1
- Initial release of Glasswave Desktop for Fedora Linux KDE Plasma 6 Wayland.
