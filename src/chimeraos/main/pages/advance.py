#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os
import gi
from component import AsyncActionFullButton
import utils


class AdvancePage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.product_name = utils.get_product_name()
        self.create_page()

    def create_page(self):
        clear_cache_button = AsyncActionFullButton(title="清除缓存", callback=utils.clear_cache)
        self.pack_start(clear_cache_button, False, False, 0)

        boot_repair_button = AsyncActionFullButton(title="修复项启动", callback=utils.boot_repair)
        self.pack_start(boot_repair_button, False, False, 0)

        etc_repair_button = AsyncActionFullButton(title="修复 /etc", callback=utils.etc_repair)
        self.pack_start(etc_repair_button, False, False, 0)

        etc_repair_full_button = AsyncActionFullButton(title="修复 /etc (完全)", callback=utils.etc_repair_full)
        self.pack_start(etc_repair_full_button, False, False, 0)

        make_swapfile = AsyncActionFullButton(title="重新创建 swapfile", callback=utils.make_swapfile)
        self.pack_start(make_swapfile, False, False, 0)
