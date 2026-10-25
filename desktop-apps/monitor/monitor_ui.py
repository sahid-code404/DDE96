#!/usr/bin/env python3
"""Glasswave Activity Monitor UI.

macOS Activity Monitor-inspired system resource and process management tool.
"""

import sys
from pathlib import Path

# Candidate module search paths for in-tree and installed runtime
candidate_dirs = [
    Path(__file__).resolve().parent,
    Path(__file__).resolve().parent.parent / "desktop-apps" / "monitor",
    Path.home() / ".local" / "share" / "glasswave" / "lib",
    Path("/usr/local/share/glasswave/lib"),
    Path("/usr/share/glasswave/lib"),
]
for d in candidate_dirs:
    if d.exists() and str(d) not in sys.path:
        sys.path.insert(0, str(d))

from monitor_engine import SystemMonitorEngine

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, Gio, GLib

CSS = """
/* Glasswave Monitor CSS */
window.monitor-window {
    background-color: #1c1c1e;
    color: #ffffff;
}

.monitor-card {
    background-color: rgba(44, 44, 46, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 14px;
    margin: 8px 14px;
}

.metric-big {
    font-size: 28px;
    font-weight: 700;
    color: #0a84ff;
}

.proc-row:selected {
    background-color: #0a84ff;
    color: #ffffff;
}
"""

class GlasswaveMonitorApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.glasswave.monitor",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.engine = SystemMonitorEngine()
        self.win = None
        self.selected_pid = None

    def do_startup(self):
        super().do_startup()
        provider = Gtk.CssProvider()
        provider.load_from_string(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_activate(self):
        self.win = Adw.ApplicationWindow(application=self)
        self.win.add_css_class("monitor-window")
        self.win.set_title("Activity Monitor")
        self.win.set_default_size(880, 560)

        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Header Bar
        header = Gtk.HeaderBar()
        header.set_show_title_buttons(True)

        # Search
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Filter processes...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        header.set_title_widget(self.search_entry)

        # Quit Process Button
        self.btn_quit_proc = Gtk.Button.new_from_icon_name("process-stop-symbolic")
        self.btn_quit_proc.set_tooltip_text("End Process (SIGTERM / SIGKILL)")
        self.btn_quit_proc.connect("clicked", self.on_end_process)
        header.pack_end(self.btn_quit_proc)

        root_box.append(header)

        # Summary Bar (CPU, Memory, Disk)
        summary_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        summary_card.add_css_class("monitor-card")

        # CPU Box
        cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        cpu_box.append(Gtk.Label(label="CPU Usage", xalign=0))
        self.lbl_cpu = Gtk.Label(label="0.0%")
        self.lbl_cpu.add_css_class("metric-big")
        cpu_box.append(self.lbl_cpu)
        summary_card.append(cpu_box)

        # Memory Box
        mem_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        mem_box.append(Gtk.Label(label="Memory Used", xalign=0))
        self.lbl_mem = Gtk.Label(label="0 / 0 GB")
        self.lbl_mem.add_css_class("metric-big")
        mem_box.append(self.lbl_mem)
        summary_card.append(mem_box)

        # Disk Box
        disk_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        disk_box.append(Gtk.Label(label="Disk Space", xalign=0))
        self.lbl_disk = Gtk.Label(label="0%")
        self.lbl_disk.add_css_class("metric-big")
        disk_box.append(self.lbl_disk)
        summary_card.append(disk_box)

        root_box.append(summary_card)

        # Process Table ListBox
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)

        self.proc_list_box = Gtk.ListBox()
        self.proc_list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.proc_list_box.connect("row-selected", self.on_proc_selected)
        scrolled.set_child(self.proc_list_box)
        root_box.append(scrolled)

        # Status Bar
        self.status_bar = Gtk.Label(label="Ready")
        self.status_bar.set_xalign(0)
        self.status_bar.set_margin_start(14)
        self.status_bar.set_margin_bottom(6)
        root_box.append(self.status_bar)

        self.win.set_content(root_box)
        self.update_metrics()
        GLib.timeout_add_seconds(2, self.update_metrics)
        self.win.present()

    def update_metrics(self):
        cpu = self.engine.get_cpu_metrics()
        self.lbl_cpu.set_text(f"{cpu['total_percent']}%")

        mem = self.engine.get_memory_metrics()
        used_gb = mem['used_mb'] / 1024.0
        total_gb = mem['total_mb'] / 1024.0
        self.lbl_mem.set_text(f"{used_gb:.1f} / {total_gb:.1f} GB")

        disk = self.engine.get_disk_metrics()
        self.lbl_disk.set_text(f"{disk['percent']}%")

        query = self.search_entry.get_text().strip()
        procs = self.engine.get_processes(query=query, limit=50)

        # Clear and repopulate
        while child := self.proc_list_box.get_first_child():
            self.proc_list_box.remove(child)

        for p in procs:
            row = Gtk.ListBoxRow()
            row.add_css_class("proc-row")
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
            box.set_margin_start(16)
            box.set_margin_end(16)
            box.set_margin_top(4)
            box.set_margin_bottom(4)

            lbl_name = Gtk.Label(label=p["name"], xalign=0)
            lbl_name.set_hexpand(True)
            box.append(lbl_name)

            lbl_pid = Gtk.Label(label=str(p["pid"]))
            lbl_pid.set_size_request(60, -1)
            box.append(lbl_pid)

            lbl_user = Gtk.Label(label=p["user"])
            lbl_user.set_size_request(70, -1)
            box.append(lbl_user)

            lbl_mem_p = Gtk.Label(label=f"{p['rss_mb']} MB")
            lbl_mem_p.set_size_request(80, -1)
            box.append(lbl_mem_p)

            row.set_child(box)
            row._pid = p["pid"]
            row._name = p["name"]
            row._user_owned = p["is_user_owned"]
            self.proc_list_box.append(row)

        return True

    def on_proc_selected(self, lb, row):
        if row and hasattr(row, "_pid"):
            self.selected_pid = row._pid
            self.selected_name = row._name
            self.selected_user_owned = row._user_owned
        else:
            self.selected_pid = None

    def on_search_changed(self, entry):
        self.update_metrics()

    def on_end_process(self, btn):
        if not self.selected_pid:
            self.status_bar.set_text("Please select a process to terminate.")
            return

        success, msg = self.engine.terminate_process(self.selected_pid, force=False)
        self.status_bar.set_text(msg)
        self.update_metrics()

def main():
    if "--check" in sys.argv:
        print("Glasswave Activity Monitor syntax and initialization OK")
        return 0
    app = GlasswaveMonitorApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
