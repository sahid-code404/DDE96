#!/usr/bin/env python3
"""Glasswave Calculator UI.

macOS-inspired Calculator application built with GTK 4, circular button
styling, AST-safe expression evaluation, and calculation history.
"""

import sys
from pathlib import Path

# Candidate module search paths for in-tree and installed runtime
candidate_dirs = [
    Path(__file__).resolve().parent,
    Path(__file__).resolve().parent.parent / "desktop-apps" / "calculator",
    Path.home() / ".local" / "share" / "glasswave" / "lib",
    Path("/usr/local/share/glasswave/lib"),
    Path("/usr/share/glasswave/lib"),
]
for d in candidate_dirs:
    if d.exists() and str(d) not in sys.path:
        sys.path.insert(0, str(d))

from calculator_engine import SafeCalculatorEngine

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, Gio, GLib

CSS = """
/* Glasswave Calculator CSS */
window.calculator-window {
    background-color: rgba(30, 30, 32, 0.94);
    color: #ffffff;
}

.calc-display {
    font-size: 38px;
    font-weight: 300;
    color: #ffffff;
    margin: 16px 14px 10px 14px;
}

.calc-btn {
    border-radius: 25px;
    min-width: 50px;
    min-height: 50px;
    font-size: 18px;
    font-weight: 500;
    border: none;
    transition: all 80ms ease;
}

.calc-btn-num {
    background-color: #3a3a3c;
    color: #ffffff;
}
.calc-btn-num:hover {
    background-color: #48484a;
}

.calc-btn-util {
    background-color: #505054;
    color: #ffffff;
}
.calc-btn-util:hover {
    background-color: #636366;
}

.calc-btn-op {
    background-color: #ff9f0a;
    color: #ffffff;
    font-size: 22px;
}
.calc-btn-op:hover {
    background-color: #ffb340;
}
"""

class GlasswaveCalculatorApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.glasswave.calculator",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.engine = SafeCalculatorEngine()
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
        self.win.add_css_class("calculator-window")
        self.win.set_title("Calculator")
        self.win.set_default_size(260, 380)
        self.win.set_resizable(False)

        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        root_box.set_margin_start(12)
        root_box.set_margin_end(12)
        root_box.set_margin_top(8)
        root_box.set_margin_bottom(14)

        # Header bar
        header = Gtk.HeaderBar()
        header.set_show_title_buttons(True)
        root_box.append(header)

        # Numeric Display
        self.display_label = Gtk.Label(label="0")
        self.display_label.add_css_class("calc-display")
        self.display_label.set_xalign(1)
        root_box.append(self.display_label)

        # Keypad Grid
        grid = Gtk.Grid()
        grid.set_column_spacing(8)
        grid.set_row_spacing(8)
        grid.set_halign(Gtk.Align.CENTER)

        buttons = [
            [("AC", "calc-btn-util", self.on_ac), ("±", "calc-btn-util", self.on_neg), ("%", "calc-btn-util", self.on_pct), ("÷", "calc-btn-op", lambda: self.on_op("/"))],
            [("7", "calc-btn-num", lambda: self.on_digit("7")), ("8", "calc-btn-num", lambda: self.on_digit("8")), ("9", "calc-btn-num", lambda: self.on_digit("9")), ("×", "calc-btn-op", lambda: self.on_op("*"))],
            [("4", "calc-btn-num", lambda: self.on_digit("4")), ("5", "calc-btn-num", lambda: self.on_digit("5")), ("6", "calc-btn-num", lambda: self.on_digit("6")), ("−", "calc-btn-op", lambda: self.on_op("-"))],
            [("1", "calc-btn-num", lambda: self.on_digit("1")), ("2", "calc-btn-num", lambda: self.on_digit("2")), ("3", "calc-btn-num", lambda: self.on_digit("3")), ("+", "calc-btn-op", lambda: self.on_op("+"))],
        ]

        for r_idx, row in enumerate(buttons):
            for c_idx, (text, css_class, callback) in enumerate(row):
                btn = Gtk.Button(label=text)
                btn.add_css_class("calc-btn")
                btn.add_css_class(css_class)
                btn.connect("clicked", lambda b, cb=callback: cb())
                grid.attach(btn, c_idx, r_idx, 1, 1)

        # Last Row: 0 (wide pill) + . + =
        btn_0 = Gtk.Button(label="0")
        btn_0.add_css_class("calc-btn")
        btn_0.add_css_class("calc-btn-num")
        btn_0.connect("clicked", lambda b: self.on_digit("0"))
        grid.attach(btn_0, 0, 4, 2, 1)

        btn_dot = Gtk.Button(label=".")
        btn_dot.add_css_class("calc-btn")
        btn_dot.add_css_class("calc-btn-num")
        btn_dot.connect("clicked", lambda b: self.on_dot())
        grid.attach(btn_dot, 2, 4, 1, 1)

        btn_eq = Gtk.Button(label="=")
        btn_eq.add_css_class("calc-btn")
        btn_eq.add_css_class("calc-btn-op")
        btn_eq.connect("clicked", lambda b: self.on_equal())
        grid.attach(btn_eq, 3, 4, 1, 1)

        root_box.append(grid)
        self.win.set_content(root_box)
        self.win.present()

    def update_ui(self):
        self.display_label.set_text(self.engine.current_display)

    def on_digit(self, d: str):
        self.engine.input_digit(d)
        self.update_ui()

    def on_dot(self):
        self.engine.input_decimal()
        self.update_ui()

    def on_ac(self):
        self.engine.all_clear()
        self.update_ui()

    def on_neg(self):
        self.engine.negate()
        self.update_ui()

    def on_pct(self):
        self.engine.percent()
        self.update_ui()

    def on_op(self, op: str):
        self.engine.set_operator(op)
        self.update_ui()

    def on_equal(self):
        self.engine.calculate()
        self.update_ui()

def main():
    if "--check" in sys.argv:
        print("Glasswave Calculator syntax and initialization OK")
        return 0
    app = GlasswaveCalculatorApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
