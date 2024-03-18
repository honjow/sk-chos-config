#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from component import AsyncActionFullButton
from config import (
    PANED_RIGHT_MARGIN_START,
    PANED_RIGHT_MARGIN_END,
    PANED_RIGHT_MARGIN_TOP,
    PANED_RIGHT_MARGIN_BOTTOM,
)

from utils import (
    clear_cache,
    boot_repair,
    re_first_run,
    etc_repair,
    etc_repair_full,
    make_swapfile,
    reset_gnome,
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
        clear_cache_button = AsyncActionFullButton(
            title="清除缓存", callback=clear_cache
        )
        self.pack_start(clear_cache_button, False, False, 0)

        boot_repair_button = AsyncActionFullButton(
            title="修复启动项", callback=boot_repair
        )
        self.pack_start(boot_repair_button, False, False, 0)

        re_first_run_button = AsyncActionFullButton(
            title="重新运行首次自动配置脚本",
            description="从预下载路径中安装Decky、Decky插件、手柄映射等。初始化Sk-ChimeraOS的一些用户配置",
            callback=re_first_run,
        )
        self.pack_start(re_first_run_button, False, False, 0)

        etc_repair_button = AsyncActionFullButton(
            title="修复 /etc",
            description="如果睡眠后立即唤醒, 可以尝试修复",
            callback=etc_repair,
        )
        self.pack_start(etc_repair_button, False, False, 0)

        etc_repair_full_button = AsyncActionFullButton(
            title="修复 /etc (完全)",
            description="重启后需要重新配置网络连接等配置",
            callback=etc_repair_full,
        )
        self.pack_start(etc_repair_full_button, False, False, 0)

        make_swapfile_button = AsyncActionFullButton(
            title="重新创建 swapfile", callback=make_swapfile
        )
        self.pack_start(make_swapfile_button, False, False, 0)

        reset_gnome_button = AsyncActionFullButton(
            title="重置 Gnome 桌面", callback=reset_gnome
        )
        self.pack_start(reset_gnome_button, False, False, 0)
