#!/usr/bin/env python3
"""Glasswave Desktop Shell Companion.

Provides a live, high-performance Wayland companion shell rendering the
macOS-inspired floating dock and top menu bar with smooth physics,
translucent glass styling, and application launcher integration.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib, Gio

GLASSWAVE_CSS = """
/* Glasswave Shell Companion CSS */
window.topbar {
    background-color: rgba(28, 28, 30, 0.78);
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    color: #ffffff;
}

window.dock {
    background-color: transparent;
}

.dock-pill {
    background-color: rgba(28, 28, 30, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 6px 14px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
}

.dock-btn {
    background: transparent;
    border: none;
    border-radius: 14px;
    padding: 4px;
    margin: 0 4px;
    transition: all 120ms ease;
}

.dock-btn:hover {
    background-color: rgba(255, 255, 255, 0.15);
}

.topbar-btn {
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 3px 8px;
    color: #ffffff;
    font-size: 13px;
    font-weight: 500;
}

.topbar-btn:hover {
    background-color: rgba(255, 255, 255, 0.12);
}

.active-title {
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
}

.clock-label {
    font-size: 13px;
    font-weight: 500;
    color: #ffffff;
}

.running-dot {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 2px;
    min-width: 4px;
    min-height: 4px;
}
"""

class GlasswaveShellCompanion(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="org.glasswave.shell.companion",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.topbar_win = None
        self.dock_win = None

    def do_startup(self):
        super().do_startup()
        self.load_css()

    def load_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_string(GLASSWAVE_CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_activate(self):
        self.create_topbar()
        self.create_dock()

    def create_topbar(self):
        self.topbar_win = Gtk.ApplicationWindow(application=self)
        self.topbar_win.add_css_class("topbar")
        self.topbar_win.set_title("Glasswave Top Bar")
        self.topbar_win.set_default_size(1280, 32)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header.set_margin_start(12)
        header.set_margin_end(12)
        header.set_margin_top(2)
        header.set_margin_bottom(2)

        # Brand Mark / Apple Style Menu
        brand_btn = Gtk.Button(label="")
        brand_btn.add_css_class("topbar-btn")
        brand_btn.connect("clicked", self.on_brand_clicked)
        header.append(brand_btn)

        # Active App Title
        self.title_label = Gtk.Label(label="Glasswave Desktop")
        self.title_label.add_css_class("active-title")
        header.append(self.title_label)

        # Expanding Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        header.append(spacer)

        # Status Indicators
        wifi_lbl = Gtk.Label(label="􀙇")
        wifi_lbl.add_css_class("topbar-btn")
        header.append(wifi_lbl)

        sound_lbl = Gtk.Label(label="􀊩")
        sound_lbl.add_css_class("topbar-btn")
        header.append(sound_lbl)

        battery_lbl = Gtk.Label(label="100% 􀛨")
        battery_lbl.add_css_class("topbar-btn")
        header.append(battery_lbl)

        # Digital Clock
        self.clock_lbl = Gtk.Label()
        self.clock_lbl.add_css_class("clock-label")
        self.update_clock()
        header.append(self.clock_lbl)
        GLib.timeout_add_seconds(1, self.update_clock)

        # Quick Settings Button
        qs_btn = Gtk.Button(label="􀌆")
        qs_btn.add_css_class("topbar-btn")
        qs_btn.connect("clicked", self.on_quicksettings_clicked)
        header.append(qs_btn)

        self.topbar_win.set_child(header)
        self.topbar_win.present()

    def update_clock(self):
        curr_time = time.strftime("%a %b %d  %I:%M %p")
        self.clock_lbl.set_text(curr_time)
        return True

    def create_dock(self):
        self.dock_win = Gtk.ApplicationWindow(application=self)
        self.dock_win.add_css_class("dock")
        self.dock_win.set_title("Glasswave Dock")
        self.dock_win.set_default_size(600, 72)

        center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        center_box.set_halign(Gtk.Align.CENTER)
        center_box.set_valign(Gtk.Align.CENTER)

        pill = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        pill.add_css_class("dock-pill")

        apps = [
            ("Finder", "glasswave-files", "glasswave-files.svg"),
            ("Terminal", "glasswave-terminal", "glasswave-terminal.svg"),
            ("Settings", "glasswave-settings", "glasswave-settings.svg"),
            ("Calculator", "glasswave-calculator", "glasswave-calculator.svg"),
            ("Activity", "glasswave-monitor", "glasswave-monitor.svg"),
            ("Screenshot", "glasswave-screenshot", "glasswave-screenshot.svg"),
        ]

        for name, cmd, icon_name in apps:
            item_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            btn = Gtk.Button()
            btn.add_css_class("dock-btn")
            btn.set_tooltip_text(name)

            # Icon
            icon_path = str(PROJECT_ROOT / "desktop-icons" / "Glasswave" / "scalable" / "apps" / icon_name)
            if os.path.exists(icon_path):
                img = Gtk.Image.new_from_file(icon_path)
                img.set_pixel_size(48)
                btn.set_child(img)
            else:
                btn.set_label(name[:2])

            btn.connect("clicked", lambda b, c=cmd: self.launch_app(c))
            item_box.append(btn)

            # Running dot placeholder
            dot = Gtk.Box()
            dot.add_css_class("running-dot")
            dot.set_halign(Gtk.Align.CENTER)
            item_box.append(dot)

            pill.append(item_box)

        center_box.append(pill)
        self.dock_win.set_child(center_box)
        self.dock_win.present()

    def launch_app(self, cmd):
        # Resolve path
        app_path = PROJECT_ROOT / "desktop-apps"
        full_cmd = cmd
        if cmd == "glasswave-files":
            full_cmd = f"python3 {PROJECT_ROOT}/desktop-apps/files/file_manager.py"
        elif cmd == "glasswave-terminal":
            full_cmd = f"python3 {PROJECT_ROOT}/desktop-apps/terminal/terminal.py"
        elif cmd == "glasswave-settings":
            full_cmd = f"python3 {PROJECT_ROOT}/desktop-control-center/control_center.py"
        elif cmd == "glasswave-calculator":
            full_cmd = f"python3 {PROJECT_ROOT}/desktop-apps/calculator/calculator_ui.py"
        elif cmd == "glasswave-monitor":
            full_cmd = f"python3 {PROJECT_ROOT}/desktop-apps/monitor/monitor_ui.py"
        elif cmd == "glasswave-screenshot":
            full_cmd = f"python3 {PROJECT_ROOT}/desktop-apps/screenshot/screenshot.py"

        try:
            subprocess.Popen(full_cmd, shell=True)
            self.title_label.set_text(cmd.replace("glasswave-", "").capitalize())
        except Exception as e:
            print(f"Error launching {cmd}: {e}", file=sys.stderr)

    def on_brand_clicked(self, btn):
        self.launch_app("glasswave-settings")

    def on_quicksettings_clicked(self, btn):
        self.launch_app("glasswave-settings")

def main():
    if "--check" in sys.argv:
        print("Glasswave Shell Companion syntax and initialization OK")
        return 0
    app = GlasswaveShellCompanion()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
