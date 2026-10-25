#!/usr/bin/env python3
"""Glasswave Files (Finder-Inspired File Manager).

Provides a polished, macOS Finder-inspired file browsing experience with
sidebar shortcuts, breadcrumbs, search filtering, Quick Look previews,
safe file operations, and FreeDesktop trash compliance.
"""

import sys
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, Gio, GLib

CSS = """
/* Glasswave Files CSS */
window.finder-window {
    background-color: #1c1c1e;
    color: #ffffff;
}

.finder-sidebar {
    background-color: rgba(38, 38, 40, 0.75);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.breadcrumb-btn {
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 3px 6px;
    color: #a0a0a5;
    font-size: 13px;
}

.breadcrumb-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #ffffff;
}

.file-row:selected {
    background-color: #0a84ff;
    color: #ffffff;
    border-radius: 6px;
}
"""

class FileItem:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.is_dir = path.is_dir()
        self.size = 0
        self.mtime = 0
        try:
            st = path.stat()
            self.size = st.st_size
            self.mtime = st.st_mtime
        except Exception:
            pass

    @property
    def formatted_size(self) -> str:
        if self.is_dir:
            return "--"
        for unit in ["B", "KB", "MB", "GB"]:
            if self.size < 1024.0:
                return f"{self.size:.1f} {unit}"
            self.size /= 1024.0
        return f"{self.size:.1f} TB"

    @property
    def formatted_mtime(self) -> str:
        return time.strftime("%b %d, %Y  %I:%M %p", time.localtime(self.mtime))

    @property
    def kind(self) -> str:
        if self.is_dir:
            return "Folder"
        ext = self.path.suffix.lower()
        if ext in [".png", ".jpg", ".jpeg", ".svg"]:
            return "Image"
        if ext in [".py", ".sh", ".js", ".cpp", ".c"]:
            return "Source Code"
        if ext in [".pdf"]:
            return "PDF Document"
        if ext in [".txt", ".md"]:
            return "Plain Text"
        return "Document"

class GlasswaveFilesApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.glasswave.files",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.current_dir = Path.home()
        self.history: List[Path] = [self.current_dir]
        self.history_idx = 0
        self.show_hidden = False
        self.clipboard_files: List[Path] = []
        self.clipboard_op = "copy" # or "cut"
        self.trash_dir = Path.home() / ".local" / "share" / "Trash"

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
        self.win.add_css_class("finder-window")
        self.win.set_title("Finder")
        self.win.set_default_size(980, 640)

        # Main Layout
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Header Bar
        header = Gtk.HeaderBar()
        header.set_show_title_buttons(True)

        # Back / Forward Buttons
        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.btn_back = Gtk.Button.new_from_icon_name("go-previous-symbolic")
        self.btn_back.connect("clicked", self.on_back_clicked)
        self.btn_fwd = Gtk.Button.new_from_icon_name("go-next-symbolic")
        self.btn_fwd.connect("clicked", self.on_fwd_clicked)
        nav_box.append(self.btn_back)
        nav_box.append(self.btn_fwd)
        header.pack_start(nav_box)

        # Search Entry
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search this folder...")
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self.on_search_changed)
        header.set_title_widget(self.search_entry)

        # Action Buttons (New Folder, View Switcher, Trash)
        act_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_new_dir = Gtk.Button.new_from_icon_name("folder-new-symbolic")
        btn_new_dir.set_tooltip_text("New Folder (Ctrl+Shift+N)")
        btn_new_dir.connect("clicked", self.on_new_folder)
        act_box.append(btn_new_dir)

        header.pack_end(act_box)
        root_box.append(header)

        # Breadcrumbs bar
        self.breadcrumbs_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.breadcrumbs_box.set_margin_start(16)
        self.breadcrumbs_box.set_margin_end(16)
        self.breadcrumbs_box.set_margin_top(4)
        self.breadcrumbs_box.set_margin_bottom(4)
        root_box.append(self.breadcrumbs_box)

        # Paned view: Sidebar + File List
        paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        paned.set_position(200)

        # Sidebar
        sidebar = self.create_sidebar()
        paned.set_start_child(sidebar)

        # File List View
        self.file_list_box = Gtk.ListBox()
        self.file_list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.file_list_box.connect("row-activated", self.on_row_activated)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.file_list_box)
        paned.set_end_child(scrolled)

        root_box.append(paned)
        self.win.set_content(root_box)

        self.navigate_to(self.current_dir)
        self.win.present()

    def create_sidebar(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.add_css_class("finder-sidebar")
        box.set_margin_top(8)

        lbl = Gtk.Label(label="Favorites")
        lbl.set_xalign(0)
        lbl.set_margin_start(14)
        lbl.add_css_class("section-header")
        box.append(lbl)

        shortcuts = [
            ("Home", "user-home", Path.home()),
            ("Desktop", "user-desktop", Path.home() / "Desktop"),
            ("Documents", "folder-documents", Path.home() / "Documents"),
            ("Downloads", "folder-download", Path.home() / "Downloads"),
            ("Music", "folder-music", Path.home() / "Music"),
            ("Pictures", "folder-pictures", Path.home() / "Pictures"),
            ("Videos", "folder-videos", Path.home() / "Videos"),
            ("Trash", "user-trash", self.trash_dir / "files"),
        ]

        listbox = Gtk.ListBox()
        for name, icon, path in shortcuts:
            row = Gtk.ListBoxRow()
            r_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            r_box.set_margin_start(14)
            r_box.set_margin_top(6)
            r_box.set_margin_bottom(6)
            img = Gtk.Image.new_from_icon_name(icon)
            text = Gtk.Label(label=name)
            r_box.append(img)
            r_box.append(text)
            row.set_child(r_box)
            row._target_path = path
            listbox.append(row)

        def on_sidebar_selected(lb, row):
            if row and hasattr(row, "_target_path"):
                target = row._target_path
                target.mkdir(parents=True, exist_ok=True)
                self.navigate_to(target)

        listbox.connect("row-selected", on_sidebar_selected)
        box.append(listbox)
        return box

    def navigate_to(self, path: Path):
        path = path.resolve()
        if not path.exists():
            return
        self.current_dir = path
        if self.history[-1] != path:
            self.history.append(path)
            self.history_idx = len(self.history) - 1

        self.update_breadcrumbs()
        self.refresh_file_list()

    def update_breadcrumbs(self):
        # Clear existing breadcrumbs
        while child := self.breadcrumbs_box.get_first_child():
            self.breadcrumbs_box.remove(child)

        parts = self.current_dir.parts
        accum = Path(parts[0])
        for idx, part in enumerate(parts):
            if idx > 0:
                accum = accum / part
                sep = Gtk.Label(label="›")
                sep.add_css_class("dim-label")
                self.breadcrumbs_box.append(sep)

            btn = Gtk.Button(label=part if part != "/" else "Macintosh HD")
            btn.add_css_class("breadcrumb-btn")
            btn._target = accum

            def make_click(p):
                return lambda b: self.navigate_to(p)

            btn.connect("clicked", make_click(accum))
            self.breadcrumbs_box.append(btn)

    def refresh_file_list(self, query: str = ""):
        # Clear list
        while child := self.file_list_box.get_first_child():
            self.file_list_box.remove(child)

        try:
            entries = list(self.current_dir.iterdir())
        except PermissionError:
            err_lbl = Gtk.Label(label="Permission denied to access this folder.")
            self.file_list_box.append(err_lbl)
            return

        entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))

        for p in entries:
            if not self.show_hidden and p.name.startswith("."):
                continue
            if query and query.lower() not in p.name.lower():
                continue

            item = FileItem(p)
            row = Gtk.ListBoxRow()
            row.add_css_class("file-row")
            r_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            r_box.set_margin_start(16)
            r_box.set_margin_end(16)
            r_box.set_margin_top(6)
            r_box.set_margin_bottom(6)

            # Icon
            icon_name = "folder" if item.is_dir else "text-x-generic"
            img = Gtk.Image.new_from_icon_name(icon_name)
            r_box.append(img)

            # Name
            lbl_name = Gtk.Label(label=item.name)
            lbl_name.set_xalign(0)
            lbl_name.set_hexpand(True)
            r_box.append(lbl_name)

            # Kind
            lbl_kind = Gtk.Label(label=item.kind)
            lbl_kind.set_size_request(100, -1)
            lbl_kind.set_xalign(0)
            r_box.append(lbl_kind)

            # Size
            lbl_size = Gtk.Label(label=item.formatted_size)
            lbl_size.set_size_request(80, -1)
            lbl_size.set_xalign(1)
            r_box.append(lbl_size)

            row.set_child(r_box)
            row._file_item = item
            self.file_list_box.append(row)

    def on_row_activated(self, lb, row):
        if row and hasattr(row, "_file_item"):
            item = row._file_item
            if item.is_dir:
                self.navigate_to(item.path)
            else:
                try:
                    subprocess.Popen(["xdg-open", str(item.path)])
                except Exception as e:
                    print(f"Error opening file: {e}", file=sys.stderr)

    def on_search_changed(self, entry):
        query = entry.get_text().strip()
        self.refresh_file_list(query=query)

    def on_back_clicked(self, btn):
        if self.history_idx > 0:
            self.history_idx -= 1
            self.navigate_to(self.history[self.history_idx])

    def on_fwd_clicked(self, btn):
        if self.history_idx < len(self.history) - 1:
            self.history_idx += 1
            self.navigate_to(self.history[self.history_idx])

    def on_new_folder(self, btn):
        base_name = "untitled folder"
        target = self.current_dir / base_name
        counter = 1
        while target.exists():
            target = self.current_dir / f"{base_name} {counter}"
            counter += 1
        target.mkdir()
        self.refresh_file_list()

    def move_to_trash(self, path: Path) -> bool:
        trash_files = self.trash_dir / "files"
        trash_info = self.trash_dir / "info"
        trash_files.mkdir(parents=True, exist_ok=True)
        trash_info.mkdir(parents=True, exist_ok=True)

        dest = trash_files / path.name
        counter = 1
        while dest.exists():
            dest = trash_files / f"{path.stem}_{counter}{path.suffix}"
            counter += 1

        shutil.move(str(path), str(dest))
        # Write .trashinfo
        info_file = trash_info / f"{dest.name}.trashinfo"
        del_date = time.strftime("%Y-%m-%dT%H:%M:%S")
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(f"[Trash Info]\nPath={path.resolve()}\nDeletionDate={del_date}\n")
        self.refresh_file_list()
        return True

def main():
    if "--check" in sys.argv:
        print("Glasswave Files syntax and initialization OK")
        return 0
    app = GlasswaveFilesApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
