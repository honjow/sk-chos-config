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


class DeckyManagerPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.product_name = PRODUCT_NAME
        self.create_page()

    def create_page(self):
        item_power_control_bin = ManagerItem(
            "PowerControl",
            "掌机功耗性能管理Decky插件",
            lambda: check_decky_plugin_exists("PowerControl"),
            installs.power_control_bin_install,
            lambda: installs.remove_decky_plugin("PowerControl"),
        )
        self.pack_start(item_power_control_bin, False, False, 0)

        if IS_HHD_SUPPORT:
            item_hhd_decky_bin = ManagerItem(
                "HHD Decky",
                "配合 HHD 使用",
                lambda: check_decky_plugin_exists("hhd-decky-bin"),
                installs.power_control_bin_install,
                lambda: installs.remove_decky_plugin("hhd-decky-bin"),
            )
            self.pack_start(item_hhd_decky_bin, False, False, 0)

        if self.product_name in ("83E1",):
            item_spb_lego = ManagerItem(
                "SBP-Legion-Go-Theme",
                "配合 HHD 使用的 CSS Loader 皮肤, 把模拟的 PS5 按钮显示为 Legion Go 的样式",
                installs.spb_lego_exist,
                installs.spb_lego_install,
                installs.spb_lego_uninstall,
            )
            self.pack_start(item_spb_lego, False, False, 0)

        if IS_HHD_SUPPORT:
            item_ps5_to_h = ManagerItem(
                "SBP-PS5-to-Handheld",
                "配合 HHD 使用的 CSS Loader 皮肤, 整合了 ROG Ally 和其它掌机以及 XBox 的样式",
                installs.ps5_to_h_exist,
                installs.ps5_to_h_install,
                installs.ps5_to_h_uninstall,
            )
            self.pack_start(item_ps5_to_h, False, False, 0)

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
            item_huesync_bin = ManagerItem(
                "HueSync (原Ayaled)",
                "掌机 LED 灯控制Decky插件, 直接安装版",
                lambda: check_decky_plugin_exists("HueSync"),
                installs.huesync_bin_install,
                lambda: installs.remove_decky_plugin("HueSync"),
            )
            self.pack_start(item_huesync_bin, False, False, 0)


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

        item_tomoon = ManagerItem(
            "ToMoon",
            "网络加速Decky插件",
            lambda: check_decky_plugin_exists("tomoon"),
            installs.tomoon_install,
            lambda: installs.remove_decky_plugin("tomoon"),
        )
        self.pack_start(item_tomoon, False, False, 0)
