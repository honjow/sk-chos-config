#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os
import gi
from component import AsyncActionFullButton
import installs
import utils

from utils import (
    check_service_autostart,
    get_product_name,
)


class AdvancePage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.product_name = get_product_name()
        self.create_page()

    def create_page(self):
        clear_cache_button = AsyncActionFullButton(title="清除缓存", callback=utils.clear_cache)
        self.pack_start(clear_cache_button, False, False, 0)
