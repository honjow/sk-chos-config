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


class ToolManagerPage(Gtk.Box):
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

        item_decky_cn = ManagerItem(
            "Decky(CN源)",
            "游戏模式的插件平台",
            lambda: check_service_exists("plugin_loader.service"),
            installs.simple_cn_decky_install,
        )
        self.pack_start(item_decky_cn, False, False, 0)

        item_handycon = ManagerItem(
            "HandyGCCS",
            "驱动部分掌机的手柄按钮",
            lambda: check_service_exists("handycon.service"),
            installs.handycon_install,
            installs.handycon_uninstall,
        )
        self.pack_start(item_handycon, False, False, 0)

        item_simple_decky_TDP = ManagerItem(
            "SimpleDeckyTDP",
            "掌机功耗性能管理 Decky插件, 只有 TDP 相关功能",
            lambda: check_decky_plugin_exists("SimpleDeckyTDP"),
            installs.simple_decky_TDP_install,
            lambda: installs.remove_decky_plugin("SimpleDeckyTDP"),
        )
        self.pack_start(item_simple_decky_TDP, False, False, 0)

        item_steam_patch = ManagerItem(
            "Steam-Patch",
            "通过自带TDP控制条来调节功耗",
            lambda: check_service_exists("steam-patch.service"),
            installs.steam_patch_install,
            installs.steam_patch_uninstall,
        )
        self.pack_start(item_steam_patch, False, False, 0)

        if self.product_name in (
            "AIR",
            "AIR 1S",
            "AIR Pro",
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


        item_power_control_bin = ManagerItem(
            "PowerControl",
            "掌机功耗性能管理Decky插件, 直接安装版",
            lambda: check_decky_plugin_exists("PowerControl"),
            installs.power_control_bin_install,
            lambda: installs.remove_decky_plugin("PowerControl"),
        )
        self.pack_start(item_power_control_bin, False, False, 0)

        item_power_control = ManagerItem(
            "PowerControl (编译版)",
            "下载最新github源码编译安装",
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
            "网络加速Decky插件",
            lambda: check_decky_plugin_exists("tomoon"),
            installs.tomoon_install,
            lambda: installs.remove_decky_plugin("tomoon"),
        )
        self.pack_start(item_tomoon, False, False, 0)

        item_emudeck_decky_controls = ManagerItem(
            "emudeck-decky-controls",
            "Decky Plugin to show Hotkeys in game",
            lambda: check_decky_plugin_exists("emudeck-decky-controls"),
            installs.emudeck_decky_controls_install,
            lambda: installs.remove_decky_plugin("emudeck-decky-controls"),
        )
        self.pack_start(item_emudeck_decky_controls, False, False, 0)

        # item_mesa_arch = ManagerItem(
        #     "Mesa(Arch官方源)",
        #     "Mesa显卡驱动, 使用 Arch 官方源安装",
        #     True,
        #     installs.mesa_arch_install,
        # )
        # self.pack_start(item_mesa_arch, False, False, 0)

        # item_valve_arch = ManagerItem(
        #     "Mesa(Valve 官方源)",
        #     "Mesa显卡驱动, 使用 Valve main 源安装",
        #     True,
        #     installs.mesa_valve_install,
        # )
        # self.pack_start(item_valve_arch, False, False, 0)

