#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os
import gi
from component import SwitchItem
import installs
import utils
from utils import check_service_autostart

from config import (
    IS_HHD_SUPPORT,
    PANED_RIGHT_MARGIN_START,
    PANED_RIGHT_MARGIN_END,
    PANED_RIGHT_MARGIN_TOP,
    PANED_RIGHT_MARGIN_BOTTOM,
    USER,
    VENDOR_NAME,
    PRODUCT_NAME,
)

class SwitchPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.create_page()

    def create_page(self):
        usb_wakeup_enabled = utils.chk_usb_wakeup()
        switch_item_usb_wakeup = SwitchItem(
            "USB唤醒",
            "默认启用, 如果睡眠后马上唤醒, 可以尝试禁用",
            usb_wakeup_enabled,
            installs.usb_wakeup_switch_callback,
        )

        handycon_enabled = check_service_autostart("handycon.service")
        switch_item_handycon = SwitchItem(
            "HandyGCCS",
            "用来驱动部分掌机的手柄按钮",
            handycon_enabled,
            installs.handycon_switch_callback,
            turnOnCallback = lambda: switch_item_hhd.switch.set_active(False),
        )

        hhd_enabled = check_service_autostart(f"hhd@{USER}.service")
        def hhd_turn_on_callback():
            switch_item_handycon.switch.set_active(False)
            if VENDOR_NAME == "AYANEO":
                switch_item_usb_wakeup.switch.set_active(False)
        switch_item_hhd = SwitchItem(
            "HHD",
            "Handheld Daemon, 另一个手柄驱动程序, 通过模拟 PS5 手柄支持陀螺仪和背键能等功能. 不能和 HandyGCCS 同时使用. 请配合HHD Decky插件使用.",
            hhd_enabled,
            installs.hhd_switch_callback,
            turnOnCallback = hhd_turn_on_callback,
        )

        sk_auto_keep_boot_entry_switch_enabled = check_service_autostart(
            "sk-auto-keep-boot-entry.service"
        )
        switch_item_sk_auto_keep_boot_entry_switch = SwitchItem(
            "SK Chimeraos 启动项守护服务",
            "开启后, 每次启动 Sk-Chimeraos 都会将自身启动项作为下次启动项, 解决双系统启动项维持问题。最好配合 Windows 启动到 Sk-Chimeraos 的功能使用, 否则建议关闭。",
            sk_auto_keep_boot_entry_switch_enabled,
            installs.sk_auto_keep_boot_entry_switch_callback,
        )

        hibernate_enabled = utils.chk_hibernate()
        switch_item_hibernate = SwitchItem(
            "休眠",
            "开启后按下电源键会进入休眠状态, 否则是睡眠状态",
            hibernate_enabled,
            installs.hibernate_switch_callback,
        )

        firmware_override_enabled = utils.chk_firmware_override()
        switch_item_firmware_override = SwitchItem(
            "firmware固件覆盖",
            "启用DSDT覆盖等, 用于修复部分掌机的问题，切换后需要重启。建议开启",
            firmware_override_enabled,
            installs.firmware_override_switch_callback,
        )

        aya_lc_suspend_file = "/etc/handygccs/special_suspend"
        aya_lc_suspend_enabled = os.path.isfile(aya_lc_suspend_file)
        switch_item_aya_lc_suspend = SwitchItem(
            "AYANEO LC键睡眠",
            "默认为截图, 开启后LC键作为睡眠键(需要开启HandyGCCS)",
            aya_lc_suspend_enabled,
            installs.aya_lc_suspend_switch_callback,
        )
        

        # layout
        self.pack_start(switch_item_handycon, False, False, 0)
        if IS_HHD_SUPPORT:
            self.pack_start(switch_item_hhd, False, False, 0)
        self.pack_start(switch_item_sk_auto_keep_boot_entry_switch, False, False, 0)
        self.pack_start(switch_item_hibernate, False, False, 0)
        self.pack_start(switch_item_firmware_override, False, False, 0)
        self.pack_start(switch_item_usb_wakeup, False, False, 0)
        if PRODUCT_NAME in (
            "AIR",
            "AIR 1S",
            "AIR Pro",
            "AIR Plus",
            "AYANEO 2",
            "GEEK",
            "GEEK 1S",
            "AYANEO 2S",
        ):
            self.pack_start(switch_item_aya_lc_suspend, False, False, 0)