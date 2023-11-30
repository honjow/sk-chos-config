#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import gi
from component import ManagerItem
import installs

from utils import (
    check_emudeck_exists,
)


class SoftManagerPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.create_page()

    def create_page(self):
        item_emudeck = ManagerItem(
            "EmuDeck",
            "模拟器整合平台",
            lambda: check_emudeck_exists(),
            installs.emudeck_install,
        )
        self.pack_start(item_emudeck, False, False, 0)

        item_this_app = ManagerItem(
            "本程序", "Sk ChimeraOS Tool", True, installs.this_app_install
        )
        self.pack_start(item_this_app, False, False, 0)