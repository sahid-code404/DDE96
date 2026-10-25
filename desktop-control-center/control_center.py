#!/usr/bin/env python3
"""Glasswave Settings & Appearance Center.

macOS System Settings-inspired desktop configuration center built on
GTK 4 and Libadwaita with frosted glass styling and instant persistence.
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

# Candidate module search paths for in-tree and installed runtime
candidate_dirs = [
    Path(__file__).resolve().parent,
    Path(__file__).resolve().parent.parent / "desktop-settings",
    Path.home() / ".local" / "share" / "glasswave" / "lib",
    Path("/usr/local/share/glasswave/lib"),
    Path("/usr/share/glasswave/lib"),
]
for d in candidate_dirs:
    if d.exists() and str(d) not in sys.path:
        sys.path.insert(0, str(d))

from settings_manager import SettingsManager

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, Gio, GLib

CSS = """
/* Glasswave Control Center CSS */
window.settings-window {
    background-color: #1c1c1e;
    color: #ffffff;
}

.navigation-sidebar {
    background-color: rgba(38, 38, 40, 0.75);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.settings-card {
    background-color: rgba(44, 44, 46, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}

.section-header {
    font-size: 14px;
    font-weight: 700;
    color: #a0a0a5;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.color-dot {
    border-radius: 12px;
    min-width: 24px;
    min-height: 24px;
    border: 2px solid transparent;
}

.color-dot:checked {
    border-color: #ffffff;
}
"""

class GlasswaveSettingsApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.glasswave.settings",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.settings = SettingsManager()
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
        self.win.add_css_class("settings-window")
        self.win.set_title("System Settings")
        self.win.set_default_size(900, 620)

        # Main Split View (Sidebar + Content)
        split_view = Adw.NavigationSplitView()

        # Content Stack
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        self.content_stack.add_named(self.create_appearance_page(), "appearance")
        self.content_stack.add_named(self.create_dock_page(), "dock")
        self.content_stack.add_named(self.create_topbar_page(), "topbar")
        self.content_stack.add_named(self.create_materials_page(), "materials")
        self.content_stack.add_named(self.create_motion_page(), "motion")
        self.content_stack.add_named(self.create_backup_page(), "backup")
        self.content_stack.add_named(self.create_about_page(), "about")

        content_page = Adw.NavigationPage.new(self.content_stack, "General")
        split_view.set_content(content_page)

        # Sidebar
        sidebar_page = Adw.NavigationPage.new(self.create_sidebar(split_view), "Settings")
        sidebar_page.set_title("Settings")
        split_view.set_sidebar(sidebar_page)

        self.win.set_content(split_view)
        self.win.present()

    def create_sidebar(self, split_view):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.add_css_class("navigation-sidebar")
        box.set_margin_top(12)
        box.set_margin_start(8)
        box.set_margin_end(8)

        categories = [
            ("Appearance", "preferences-desktop-theme", "appearance"),
            ("Desktop & Dock", "user-desktop", "dock"),
            ("Top Menu Bar", "preferences-desktop-display", "topbar"),
            ("Blur & Materials", "preferences-system-windows", "materials"),
            ("Accessibility & Motion", "preferences-desktop-accessibility", "motion"),
            ("Backup & Restore", "document-save", "backup"),
            ("About & System", "help-about", "about"),
        ]

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)

        for label, icon, tag in categories:
            row = Gtk.ListBoxRow()
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            row_box.set_margin_start(12)
            row_box.set_margin_end(12)
            row_box.set_margin_top(8)
            row_box.set_margin_bottom(8)

            img = Gtk.Image.new_from_icon_name(icon)
            lbl = Gtk.Label(label=label)
            lbl.set_xalign(0)

            row_box.append(img)
            row_box.append(lbl)
            row.set_child(row_box)
            row._tag = tag
            listbox.append(row)

        def on_row_selected(lb, row):
            if row:
                self.content_stack.set_visible_child_name(row._tag)

        listbox.connect("row-selected", on_row_selected)
        listbox.select_row(listbox.get_row_at_index(0))
        box.append(listbox)
        return box

    def create_appearance_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)

        title = Gtk.Label(label="Appearance")
        title.set_xalign(0)
        title.add_css_class("title-1")
        page.append(title)

        # Light / Dark Switcher Card
        card_theme = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card_theme.add_css_class("settings-card")

        lbl_theme = Gtk.Label(label="Desktop Appearance Mode")
        lbl_theme.set_xalign(0)
        card_theme.append(lbl_theme)

        theme_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        dark_btn = Gtk.CheckButton(label="Dark Mode (Glasswave Dark)")
        light_btn = Gtk.CheckButton(label="Light Mode (Glasswave Light)")
        light_btn.set_group(dark_btn)

        curr_theme = self.settings.get("appearance", "theme", "dark")
        if curr_theme == "dark":
            dark_btn.set_active(True)
        else:
            light_btn.set_active(True)

        def on_theme_toggled(btn):
            if dark_btn.get_active():
                self.settings.set("appearance", "theme", "dark")
            else:
                self.settings.set("appearance", "theme", "light")
            self.settings.sync_to_system()

        dark_btn.connect("toggled", on_theme_toggled)
        light_btn.connect("toggled", on_theme_toggled)

        theme_box.append(dark_btn)
        theme_box.append(light_btn)
        card_theme.append(theme_box)
        page.append(card_theme)

        # Accent Color Card
        card_accent = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card_accent.add_css_class("settings-card")
        lbl_acc = Gtk.Label(label="Accent Color")
        lbl_acc.set_xalign(0)
        card_accent.append(lbl_acc)

        accent_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        accents = [
            ("blue", "#0a84ff"),
            ("purple", "#5e5ce6"),
            ("pink", "#ff375f"),
            ("orange", "#ff9f0a"),
            ("green", "#30d158"),
            ("graphite", "#8e8e93"),
        ]
        curr_accent = self.settings.get("appearance", "accent_color", "blue")
        group_btn = None
        for name, hex_code in accents:
            btn = Gtk.CheckButton()
            btn.add_css_class("color-dot")
            btn.set_tooltip_text(name.capitalize())
            if group_btn is None:
                group_btn = btn
            else:
                btn.set_group(group_btn)
            if name == curr_accent:
                btn.set_active(True)

            def make_handler(acc_name):
                return lambda b: self.settings.set("appearance", "accent_color", acc_name) if b.get_active() else None

            btn.connect("toggled", make_handler(name))
            accent_box.append(btn)

        card_accent.append(accent_box)
        page.append(card_accent)
        return page

    def create_dock_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)

        title = Gtk.Label(label="Desktop & Dock")
        title.set_xalign(0)
        title.add_css_class("title-1")
        page.append(title)

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        card.add_css_class("settings-card")

        # Icon Size Slider
        lbl_size = Gtk.Label(label="Dock Icon Size (Pixels)")
        lbl_size.set_xalign(0)
        card.append(lbl_size)

        curr_size = self.settings.get("dock", "icon_size", 52)
        size_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 32, 96, 4)
        size_scale.set_value(curr_size)
        size_scale.set_draw_value(True)
        size_scale.connect("value-changed", lambda s: self.settings.set("dock", "icon_size", int(s.get_value())))
        card.append(size_scale)

        # Magnification Slider
        lbl_zoom = Gtk.Label(label="Hover Magnification Scale")
        lbl_zoom.set_xalign(0)
        card.append(lbl_zoom)

        curr_zoom = self.settings.get("dock", "magnification_factor", 1.35)
        zoom_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1.0, 1.8, 0.05)
        zoom_scale.set_value(curr_zoom)
        zoom_scale.set_draw_value(True)
        zoom_scale.connect("value-changed", lambda s: self.settings.set("dock", "magnification_factor", round(s.get_value(), 2)))
        card.append(zoom_scale)

        # Autohide Switch
        auto_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_auto = Gtk.Label(label="Automatically hide and show the Dock")
        lbl_auto.set_hexpand(True)
        lbl_auto.set_xalign(0)
        sw_auto = Gtk.Switch()
        sw_auto.set_active(self.settings.get("dock", "autohide", False))
        sw_auto.connect("state-set", lambda sw, st: self.settings.set("dock", "autohide", st) or False)
        auto_box.append(lbl_auto)
        auto_box.append(sw_auto)
        card.append(auto_box)

        page.append(card)
        return page

    def create_topbar_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)

        title = Gtk.Label(label="Top Menu Bar")
        title.set_xalign(0)
        title.add_css_class("title-1")
        page.append(title)

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        card.add_css_class("settings-card")

        box_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_t = Gtk.Label(label="Display active application title")
        lbl_t.set_hexpand(True)
        lbl_t.set_xalign(0)
        sw_t = Gtk.Switch()
        sw_t.set_active(self.settings.get("topbar", "show_title", True))
        sw_t.connect("state-set", lambda sw, st: self.settings.set("topbar", "show_title", st) or False)
        box_title.append(lbl_t)
        box_title.append(sw_t)
        card.append(box_title)

        box_bat = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_b = Gtk.Label(label="Display battery status & percentage")
        lbl_b.set_hexpand(True)
        lbl_b.set_xalign(0)
        sw_b = Gtk.Switch()
        sw_b.set_active(self.settings.get("topbar", "show_battery", True))
        sw_b.connect("state-set", lambda sw, st: self.settings.set("topbar", "show_battery", st) or False)
        box_bat.append(lbl_b)
        box_bat.append(sw_b)
        card.append(box_bat)

        page.append(card)
        return page

    def create_materials_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)

        title = Gtk.Label(label="Blur & Translucent Materials")
        title.set_xalign(0)
        title.add_css_class("title-1")
        page.append(title)

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        card.add_css_class("settings-card")

        # Blur Enabled
        box_blur = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_bl = Gtk.Label(label="Enable hardware-accelerated backdrop blur")
        lbl_bl.set_hexpand(True)
        lbl_bl.set_xalign(0)
        sw_bl = Gtk.Switch()
        sw_bl.set_active(self.settings.get("materials", "blur_enabled", True))
        sw_bl.connect("state-set", lambda sw, st: self.settings.set("materials", "blur_enabled", st) or False)
        box_blur.append(lbl_bl)
        box_blur.append(sw_bl)
        card.append(box_blur)

        # Blur Strength
        lbl_str = Gtk.Label(label="Blur Radius & Diffusion Strength")
        lbl_str.set_xalign(0)
        card.append(lbl_str)
        curr_str = self.settings.get("materials", "blur_strength", 8)
        scale_str = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 15, 1)
        scale_str.set_value(curr_str)
        scale_str.set_draw_value(True)
        scale_str.connect("value-changed", lambda s: self.settings.set("materials", "blur_strength", int(s.get_value())))
        card.append(scale_str)

        page.append(card)
        return page

    def create_motion_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)

        title = Gtk.Label(label="Accessibility & Motion")
        title.set_xalign(0)
        title.add_css_class("title-1")
        page.append(title)

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        card.add_css_class("settings-card")

        box_rm = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_rm = Gtk.Label(label="Reduced Motion (Disables zoom, bounce, and translations)")
        lbl_rm.set_hexpand(True)
        lbl_rm.set_xalign(0)
        sw_rm = Gtk.Switch()
        sw_rm.set_active(self.settings.get("motion", "reduced_motion", False))
        def on_rm_toggled(sw, st):
            self.settings.set("motion", "reduced_motion", st)
            self.settings.sync_to_system()
            return False
        sw_rm.connect("state-set", on_rm_toggled)
        box_rm.append(lbl_rm)
        box_rm.append(sw_rm)
        card.append(box_rm)

        page.append(card)
        return page

    def create_backup_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)

        title = Gtk.Label(label="Backup & Reset")
        title.set_xalign(0)
        title.add_css_class("title-1")
        page.append(title)

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        card.add_css_class("settings-card")

        btn_backup = Gtk.Button(label="Create Timestamped Backup Now")
        btn_backup.connect("clicked", self.on_backup_clicked)
        card.append(btn_backup)

        btn_reset = Gtk.Button(label="Reset Settings to Glasswave Defaults")
        btn_reset.connect("clicked", self.on_reset_clicked)
        card.append(btn_reset)

        self.status_lbl = Gtk.Label(label="")
        card.append(self.status_lbl)

        page.append(card)
        return page

    def on_backup_clicked(self, btn):
        bk = self.settings.backup()
        self.status_lbl.set_text(f"Backup saved to: {bk.name}")

    def on_reset_clicked(self, btn):
        self.settings.reset_to_defaults()
        self.status_lbl.set_text("All settings reset to default values.")

    def create_about_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)

        title = Gtk.Label(label="About Glasswave Desktop")
        title.set_xalign(0)
        title.add_css_class("title-1")
        page.append(title)

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("settings-card")

        card.append(Gtk.Label(label=f"OS: {platform.system()} {platform.release()} ({platform.machine()})", xalign=0))
        card.append(Gtk.Label(label="Desktop: Glasswave Desktop on KDE Plasma 6 Wayland", xalign=0))
        card.append(Gtk.Label(label=f"Wayland Display: {os.environ.get('WAYLAND_DISPLAY', 'N/A')}", xalign=0))
        card.append(Gtk.Label(label=f"Python: {platform.python_version()}", xalign=0))
        card.append(Gtk.Label(label="License: MIT License", xalign=0))
        page.append(card)

        # KDE System Settings Modules Integration Card
        kde_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        kde_card.add_css_class("settings-card")

        lbl_kde = Gtk.Label(label="Native KDE Plasma 6 System Settings Integration")
        lbl_kde.set_xalign(0)
        lbl_kde.add_css_class("heading")
        kde_card.append(lbl_kde)

        desc_kde = Gtk.Label(label="Access advanced hardware, multi-monitor display scaling, color profiles, and system services directly via KDE Control Modules.")
        desc_kde.set_wrap(True)
        desc_kde.set_xalign(0)
        kde_card.append(desc_kde)

        kde_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        def launch_kcm(cmd_args):
            try:
                subprocess.Popen(cmd_args)
            except Exception as e:
                print(f"Could not launch {cmd_args}: {e}")

        btn_screen = Gtk.Button(label="Display & Scaling (KCM)")
        btn_screen.connect("clicked", lambda b: launch_kcm(["kcmshell6", "kcm_kscreen"]))
        kde_btn_box.append(btn_screen)

        btn_colors = Gtk.Button(label="Color Schemes (KCM)")
        btn_colors.connect("clicked", lambda b: launch_kcm(["kcmshell6", "kcm_colors"]))
        kde_btn_box.append(btn_colors)

        btn_anim = Gtk.Button(label="KWin Animations (KCM)")
        btn_anim.connect("clicked", lambda b: launch_kcm(["kcmshell6", "kcm_animations"]))
        kde_btn_box.append(btn_anim)

        btn_full = Gtk.Button(label="Open Full System Settings")
        btn_full.connect("clicked", lambda b: launch_kcm(["systemsettings"]))
        kde_btn_box.append(btn_full)

        kde_card.append(kde_btn_box)
        page.append(kde_card)
        return page

def main():
    if "--check" in sys.argv:
        print("Glasswave Control Center syntax and initialization OK")
        return 0
    app = GlasswaveSettingsApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
