#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import gi
from component import ManagerItem
import installs

from utils import (
    check_decky_plugin_exists,
    check_service_exists,
)

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


class DeckyAdvanceManagerPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.product_name = PRODUCT_NAME
        self.create_page()

    def create_page(self):

        if IS_HHD_SUPPORT:
            item_hhd_decky = ManagerItem(
                "HHD Decky (编译版)",
                "配合 HHD 使用",
                lambda: check_decky_plugin_exists("hhd-decky"),
                installs.hhd_decky_install,
                lambda: installs.remove_decky_plugin("hhd-decky"),
            )
            self.pack_start(item_hhd_decky, False, False, 0)

        item_simple_decky_TDP = ManagerItem(
            "SimpleDeckyTDP",
            "掌机功耗性能管理 Decky插件, 只有 TDP 相关功能",
            lambda: check_decky_plugin_exists("SimpleDeckyTDP"),
            installs.simple_decky_TDP_install,
            lambda: installs.remove_decky_plugin("SimpleDeckyTDP"),
        )
        self.pack_start(item_simple_decky_TDP, False, False, 0)

        if (
            self.product_name
            in (
                "AIR",
                "AIR 1S",
                "AIR 1S Limited",
                "AIR Pro",
                "AYANEO 2",
                "GEEK",
                "AYANEO 2S",
                "GEEK 1S",
            )
            or IS_LED_SUPPORTED
        ):
            item_huesync = ManagerItem(
                "HueSync (原Ayaled) ",
                "掌机 LED 灯控制Decky插件, 源码编译安装",
                lambda: check_decky_plugin_exists("HueSync"),
                installs.huesync_install,
                lambda: installs.remove_decky_plugin("HueSync"),
            )
            self.pack_start(item_huesync, False, False, 0)

        # Lenovo Legion Go
        if self.product_name == "83E1":
            item_LegionGoRemapper = ManagerItem(
                "LegionGoRemapper",
                "Lenovo Legion Go 手柄按键映射, 灯光控制 Decky 插件",
                lambda: check_decky_plugin_exists("LegionGoRemapper"),
                installs.LegionGoRemapper_install,
                lambda: installs.remove_decky_plugin("LegionGoRemapper"),
            )
            self.pack_start(item_LegionGoRemapper, False, False, 0)

        item_power_control = ManagerItem(
            "PowerControl",
            "下载最新github源码编译安装",
            lambda: check_decky_plugin_exists("PowerControl"),
            installs.power_control_install,
            lambda: installs.remove_decky_plugin("PowerControl"),
        )
        self.pack_start(item_power_control, False, False, 0)
