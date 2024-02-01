#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from component import AsyncActionFullButton
import utils
from config import (
    PANED_RIGHT_MARGIN_START,
    PANED_RIGHT_MARGIN_END,
    PANED_RIGHT_MARGIN_TOP,
    PANED_RIGHT_MARGIN_BOTTOM,
)
class AdvancePage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.create_page()

    def create_page(self):
        clear_cache_button = AsyncActionFullButton(title="清除缓存", callback=utils.clear_cache)
        self.pack_start(clear_cache_button, False, False, 0)

        boot_repair_button = AsyncActionFullButton(title="修复启动项", callback=utils.boot_repair)
        self.pack_start(boot_repair_button, False, False, 0)

        etc_repair_button = AsyncActionFullButton(title="修复 /etc", callback=utils.etc_repair)
        self.pack_start(etc_repair_button, False, False, 0)

        etc_repair_full_button = AsyncActionFullButton(title="修复 /etc (完全)",
                                                       description="重启后需要重新配置网络连接, 重新安装启用Decky、手柄映射等",
                                                       callback=utils.etc_repair_full)
        self.pack_start(etc_repair_full_button, False, False, 0)

        make_swapfile_button = AsyncActionFullButton(title="重新创建 swapfile", callback=utils.make_swapfile)
        self.pack_start(make_swapfile_button, False, False, 0)

        reset_gnome_button = AsyncActionFullButton(title="重置 Gnome 桌面", callback=utils.reset_gnome)
        self.pack_start(reset_gnome_button, False, False, 0)
