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
    get_product_name,
)


class ManagerPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # self.set_margin_start(20)
        # self.set_margin_end(20)
        # self.set_margin_top(20)
        # self.set_margin_bottom(20)
        self.product_name = get_product_name()
        self.create_page()

    def create_page(self):
        item_decky = ManagerItem(
            "Decky",
            "游戏模式的插件平台",
            lambda: check_service_exists("plugin_loader.service"),
            installs.simple_decky_install,
        )
        self.pack_start(item_decky, False, False, 0)

        item_handycon = ManagerItem(
            "HandyGCCS",
            "驱动部分掌机的手柄按钮",
            lambda: check_service_exists("handycon.service"),
            installs.handycon_install,
            installs.handycon_uninstall,
        )
        self.pack_start(item_handycon, False, False, 0)

        if self.product_name in (
            "AIR",
            "AIR Pro",
            "AIR Plus",
            "AYANEO 2",
            "GEEK",
            "AYANEO 2S",
            "GEEK 1S",
        ):
            item_ayaled = ManagerItem(
                "AYANEO LED",
                "AYANEO掌机LED灯控制Decky插件",
                lambda: check_decky_plugin_exists("ayaled"),
                installs.ayaled_install,
                lambda: installs.remove_decky_plugin("ayaled"),
            )
            self.pack_start(item_ayaled, False, False, 0)

        item_power_control = ManagerItem(
            "PowerControl",
            "掌机功耗性能管理Decky插件",
            lambda: check_decky_plugin_exists("PowerControl"),
            installs.power_control_install,
            lambda: installs.remove_decky_plugin("PowerControl"),
        )
        self.pack_start(item_power_control, False, False, 0)

        item_mango_peel = ManagerItem(
            "MangoPeel",
            "性能监测自定义Decky插件",
            lambda: check_decky_plugin_exists("MangoPeel"),
            installs.mango_peel_install,
            lambda: installs.remove_decky_plugin("MangoPeel"),
        )
        self.pack_start(item_mango_peel, False, False, 0)

        item_tomoon = ManagerItem(
            "ToMoon",
            "科学上网Decky插件",
            lambda: check_decky_plugin_exists("tomoon"),
            installs.tomoon_install,
            lambda: installs.remove_decky_plugin("tomoon"),
        )
        self.pack_start(item_tomoon, False, False, 0)

        item_mesa_arch = ManagerItem(
            "Mesa(Arch官方源)",
            "Mesa显卡驱动, 使用 Arch 官方源安装",
            True,
            installs.mesa_arch_install,
        )
        self.pack_start(item_mesa_arch, False, False, 0)

        item_valve_arch = ManagerItem(
            "Mesa(Valve 官方源)",
            "Mesa显卡驱动, 使用 Valve main 源安装",
            True,
            installs.mesa_valve_install,
        )
        self.pack_start(item_valve_arch, False, False, 0)

        item_this_app = ManagerItem(
            "本程序", "SkHoloisoConfig", True, installs.this_app_install
        )
        self.pack_start(item_this_app, False, False, 0)