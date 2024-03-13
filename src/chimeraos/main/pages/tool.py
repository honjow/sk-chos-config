#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import gi
from component import ManagerItem
import installs
import utils

from config import (
    PANED_RIGHT_MARGIN_START,
    PANED_RIGHT_MARGIN_END,
    PANED_RIGHT_MARGIN_TOP,
    PANED_RIGHT_MARGIN_BOTTOM,
    IS_HHD_SUPPORT,
    IS_LED_SUPPORTED,
    PRODUCT_NAME,
    USER,
)


class ToolManagerPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.product_name = PRODUCT_NAME
        self.create_page()

    def create_page(self):
        item_decky = ManagerItem(
            "Decky",
            "游戏模式的插件平台",
            lambda: utils.check_service_exists("plugin_loader.service"),
            installs.simple_decky_install,
        )
        self.pack_start(item_decky, False, False, 0)

        item_decky_cn = ManagerItem(
            "Decky(CN源)",
            "游戏模式的插件平台",
            lambda: utils.check_service_exists("plugin_loader.service"),
            installs.simple_cn_decky_install,
        )
        self.pack_start(item_decky_cn, False, False, 0)

        item_handycon = ManagerItem(
            "HandyGCCS",
            "驱动部分掌机的手柄按钮",
            lambda: utils.check_service_exists("handycon.service"),
            installs.handycon_install,
            installs.handycon_uninstall,
        )
        self.pack_start(item_handycon, False, False, 0)

        if IS_HHD_SUPPORT:
            item_hhd = ManagerItem(
                "HHD",
                "Handheld Daemon , 另一个手柄驱动程序",
                lambda: utils.check_service_exists(f"hhd@{USER}.service"),
                installs.hhd_install,
                installs.hhd_install,
            )
            self.pack_start(item_hhd, False, False, 0)

        item_nix_ = ManagerItem(
            "Nix",
            "Nix 包管理器, 可以在不可变系统上安装软件, 系统更新不会影响软件",
            lambda: utils.check_nix_exists(),
            installs.nix_install,
            installs.nix_uninstall,
        )
        self.pack_start(item_nix_, False, False, 0)
