#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import utils
from config import (
    PANED_RIGHT_MARGIN_START,
    PANED_RIGHT_MARGIN_END,
    PANED_RIGHT_MARGIN_TOP,
    PANED_RIGHT_MARGIN_BOTTOM,
)
class AboutPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.create_page()
    
    def open_website(label, uri):
        Gdk.spawn_command_line_async(f'xdg-open {uri}')

    def create_page(self):

        # grid = Gtk.Grid()
        # grid.set_column_spacing(10)
        # grid.set_row_spacing(10)
        # grid.set_margin_top(20)
        # grid.set_margin_bottom(20)
        # grid.set_margin_start(20)
        # grid.set_margin_end(20)
        # grid.set_halign(Gtk.Align.CENTER)

        # 应用程序名称
        name_label = Gtk.Label()
        name_label.set_text("Sk ChimeraOS Config")
        name_label.set_halign(Gtk.Align.CENTER)
        name_label.set_valign(Gtk.Align.CENTER)
        name_label.set_hexpand(True)
        # name_label.set_vexpand(True)
        name_label.set_margin_bottom(10)
        name_label.set_margin_top(10)
        name_label.set_margin_start(10)
        name_label.set_margin_end(10)
        name_label.set_markup("<span font_weight='bold' font_size='large'>{}</span>".format(name_label.get_text()))
        self.pack_start(name_label, False, False, 0)


        version = utils.get_package_version("sk-chos-tool")

        # 版本号
        version_label = Gtk.Label()
        version_label.set_text(f"版本 {version}")
        version_label.set_halign(Gtk.Align.CENTER)
        version_label.set_valign(Gtk.Align.CENTER)
        self.pack_start(version_label, False, False, 0)

        # 作者
        authors_label = Gtk.Label()
        authors_label.set_text("作者: Honjow")
        authors_label.set_halign(Gtk.Align.CENTER)
        authors_label.set_valign(Gtk.Align.CENTER)
        self.pack_start(authors_label, False, False, 0)

        # 官方网站
        website_label = Gtk.Label()
        url = "https://github.com/honjow/sk-holoiso-config"
        website_label.set_markup(f"Github: <a href='{url}'>{url}</a>")
        website_label.set_halign(Gtk.Align.CENTER)
        website_label.set_valign(Gtk.Align.CENTER)
        website_label.set_use_markup(True)
        website_label.connect("activate-link", self.open_website, url)
        self.pack_start(website_label, False, False, 0)
        # website_label.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        # # 设置部件在网格中的位置
        # grid.attach(name_label, 0, 0, 2, 1)
        # grid.attach(version_label, 0, 1, 2, 1)
        # grid.attach(authors_label, 0, 2, 2, 1)
        # grid.attach(website_label, 0, 3, 2, 1)

        # self.pack_start(grid, True, True, 0)