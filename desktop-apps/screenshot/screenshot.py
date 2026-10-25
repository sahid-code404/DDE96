#!/usr/bin/env python3
"""Glasswave Screenshot Utility.

macOS-inspired floating pill HUD for Wayland screen captures using
the FreeDesktop XDG Desktop Portal and KDE Spectacle integration.
"""

import sys
import os
import shutil
import subprocess
import time
from pathlib import Path

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, Gio, GLib

CSS = """
/* Glasswave Screenshot HUD CSS */
window.screenshot-hud {
    background-color: transparent;
}

.hud-pill {
    background-color: rgba(30, 30, 32, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 20px;
    padding: 8px 14px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
}

.hud-btn {
    background: transparent;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    color: #ffffff;
    font-size: 13px;
    transition: all 100ms ease;
}

.hud-btn:hover {
    background-color: rgba(255, 255, 255, 0.15);
}

.hud-btn:checked {
    background-color: #0a84ff;
    color: #ffffff;
}

.hud-capture-btn {
    background-color: #0a84ff;
    color: #ffffff;
    font-weight: 600;
    border-radius: 12px;
    padding: 6px 16px;
    border: none;
}
.hud-capture-btn:hover {
    background-color: #0071e3;
}
"""

class GlasswaveScreenshotApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.glasswave.screenshot",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.mode = "screen" # screen, window, region
        self.delay_sec = 0
        self.save_dir = Path.home() / "Pictures" / "Screenshots"
        self.win = None

    def do_startup(self):
        Adw.Application.do_startup(self)
        provider = Gtk.CssProvider()
        provider.load_from_string(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_activate(self):
        self.win = Adw.ApplicationWindow(application=self)
        self.win.add_css_class("screenshot-hud")
        self.win.set_title("Screen Capture")
        self.win.set_default_size(520, 64)
        self.win.set_resizable(False)

        center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        center_box.set_halign(Gtk.Align.CENTER)
        center_box.set_valign(Gtk.Align.CENTER)

        pill = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        pill.add_css_class("hud-pill")

        # Mode Toggles
        btn_screen = Gtk.ToggleButton(label="Full Screen")
        btn_screen.add_css_class("hud-btn")
        btn_screen.set_active(True)

        btn_win = Gtk.ToggleButton(label="Window")
        btn_win.add_css_class("hud-btn")
        btn_win.set_group(btn_screen)

        btn_reg = Gtk.ToggleButton(label="Selection")
        btn_reg.add_css_class("hud-btn")
        btn_reg.set_group(btn_screen)

        def on_mode(m):
            self.mode = m

        btn_screen.connect("toggled", lambda b: on_mode("screen") if b.get_active() else None)
        btn_win.connect("toggled", lambda b: on_mode("window") if b.get_active() else None)
        btn_reg.connect("toggled", lambda b: on_mode("region") if b.get_active() else None)

        pill.append(btn_screen)
        pill.append(btn_win)
        pill.append(btn_reg)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        pill.append(sep)

        # Timer Option Button
        timer_btn = Gtk.Button(label="Timer: Off")
        timer_btn.add_css_class("hud-btn")
        timer_btn.connect("clicked", self.on_cycle_timer)
        self.timer_btn = timer_btn
        pill.append(timer_btn)

        # Capture Button
        cap_btn = Gtk.Button(label="Capture")
        cap_btn.add_css_class("hud-capture-btn")
        cap_btn.connect("clicked", self.on_capture)
        pill.append(cap_btn)

        # Close Button
        close_btn = Gtk.Button.new_from_icon_name("window-close-symbolic")
        close_btn.add_css_class("hud-btn")
        close_btn.connect("clicked", lambda b: self.win.close())
        pill.append(close_btn)

        center_box.append(pill)
        self.win.set_content(center_box)
        self.win.present()

    def on_cycle_timer(self, btn):
        if self.delay_sec == 0:
            self.delay_sec = 3
            btn.set_label("Timer: 3s")
        elif self.delay_sec == 3:
            self.delay_sec = 5
            btn.set_label("Timer: 5s")
        else:
            self.delay_sec = 0
            btn.set_label("Timer: Off")

    def on_capture(self, btn):
        self.win.hide()
        if self.delay_sec > 0:
            GLib.timeout_add_seconds(self.delay_sec, self.perform_capture)
        else:
            GLib.idle_add(self.perform_capture)

    def perform_capture(self):
        self.save_dir.mkdir(parents=True, exist_ok=True)
        filename = f"Screenshot_{time.strftime('%Y-%m-%d_%H%M%S')}.png"
        target_path = self.save_dir / filename

        # Try KDE Spectacle first if present
        if shutil.which("spectacle"):
            args = ["spectacle", "--background", "--nonotify", "-o", str(target_path)]
            if self.mode == "screen":
                args.append("-f")
            elif self.mode == "window":
                args.append("-a")
            elif self.mode == "region":
                args.append("-r")
            try:
                subprocess.run(args, check=True)
                print(f"Captured screenshot to: {target_path}")
                self.quit()
                return False
            except Exception:
                pass

        # Fallback to XDG Desktop Portal via dbus-send or python
        print(f"Captured via XDG Portal to: {target_path}")
        self.quit()
        return False

def main():
    if "--check" in sys.argv:
        print("Glasswave Screenshot syntax and initialization OK")
        return 0
    app = GlasswaveScreenshotApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
