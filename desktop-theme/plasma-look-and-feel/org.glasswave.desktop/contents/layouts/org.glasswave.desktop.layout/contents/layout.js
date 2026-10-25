// Glasswave Desktop - Plasma 6 Default Layout Script

var topBar = new Panel("org.kde.plasma.panel");
topBar.location = "top";
topBar.height = 32;
topBar.alignment = "center";
topBar.floating = false;

// Top Bar Applets
topBar.addWidget("org.glasswave.topbar");
topBar.addWidget("org.kde.plasma.appmenu");
var spacerTop = topBar.addWidget("org.kde.plasma.panelspacer");
spacerTop.currentConfigGroup = ["Configuration", "General"];
spacerTop.writeConfig("expanding", "true");
topBar.addWidget("org.kde.plasma.systemtray");
topBar.addWidget("org.kde.plasma.digitalclock");
topBar.addWidget("org.glasswave.quicksettings");

// Floating Bottom Dock
var dock = new Panel("org.kde.plasma.panel");
dock.location = "bottom";
dock.height = 68;
dock.alignment = "center";
dock.floating = true;
dock.hiding = "windowscover";

dock.addWidget("org.glasswave.dock");
dock.addWidget("org.kde.plasma.trash");
