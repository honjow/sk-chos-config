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

from utils import (
    check_service_autostart,
    get_product_name,
)


class SwitchPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # self.set_margin_start(20)
        # self.set_margin_end(20)
        # self.set_margin_top(20)
        # self.set_margin_bottom(20)
        self.product_name = get_product_name()
        self.create_page()

    def create_page(self):
        # is_sk_holo2 = utils.is_sk_holo2()

        handycon_enabled = check_service_autostart("handycon.service")
        switch_item_handycon = SwitchItem(
            "HandyGCCS",
            "用来驱动部分掌机的手柄按钮",
            handycon_enabled,
            installs.handycon_switch_callback,
        )
        self.pack_start(switch_item_handycon, False, False, 0)

        hibernate_enabled = utils.chk_hibernate()
        switch_item_hibernate = SwitchItem(
            "休眠",
            "开启后按下电源键会进入休眠状态, 否则是睡眠状态",
            hibernate_enabled,
            installs.hibernate_switch_callback,
        )
        self.pack_start(switch_item_hibernate, False, False, 0)

        # grub_quiet_boot_enabled = utils.chk_grub_quiet_boot()
        # switch_item_grub_quiet_boot = SwitchItem(
        #     "静默启动",
        #     "开启后启动时不显示GRUB命令行输出",
        #     grub_quiet_boot_enabled,
        #     installs.grub_quiet_boot_switch_callback,
        # )
        # self.pack_start(switch_item_grub_quiet_boot, False, False, 0)

        # override_bitrate_enabled = utils.chk_override_bitrate()
        # switch_item_override_bitrate = SwitchItem(
        #     "破音修复",
        #     "强制16bit音频输出",
        #     override_bitrate_enabled,
        #     installs.override_bitrate_switch_callback,
        # )
        # self.pack_start(switch_item_override_bitrate, False, False, 0)

        # if self.product_name == "ONEXPLAYER 2 ARP23":
        #     oxp2lsusb_enabled = check_service_autostart("oxp2-lsusb.service")
        #     switch_item_oxp2lsusb = SwitchItem(
        #         "OXP2手柄热插拔检测修复",
        #         "修复OXP2手柄热插拔后不识别的问题",
        #         oxp2lsusb_enabled,
        #         installs.oxp2lsusb_switch_callback,
        #     )
        #     self.pack_start(switch_item_oxp2lsusb, False, False, 0)

        #     oxp2_volume_button_fix_enabled = check_service_autostart(
        #         "oxp2-volume-button-fix.service"
        #     )
        #     switch_item_oxp2_volume_button_fix = SwitchItem(
        #         "OXP2音量键修复",
        #         "修复OXP2音量键问题",
        #         oxp2_volume_button_fix_enabled,
        #         installs.oxp2_volume_button_fix_switch_callback,
        #     )
        #     self.pack_start(switch_item_oxp2_volume_button_fix, False, False, 0)

        # if self.product_name in (
        #     "NEXT",
        #     "NEXT Pro",
        #     "NEXT Advance",
        #     "AYANEO NEXT",
        #     "AYANEO NEXT Pro",
        #     "AYANEO NEXT Advance",
        #     "AIR",
        #     "AIR Pro",
        #     "AIR Plus",
        #     "AYANEO 2",
        #     "GEEK",
        #     "AYANEO 2S",
        # ) and not is_sk_holo2:
        #     aya_lc_suspend_file = "/usr/share/handygccs/aya-lc-suspend"
        #     aya_lc_suspend_enabled = os.path.isfile(aya_lc_suspend_file)
        #     switch_item_aya_lc_suspend = SwitchItem(
        #         "AYANEO LC键睡眠",
        #         "默认为截图, 开启后LC键作为睡眠键(如果没有效果，请先更新HandyGCCS)",
        #         aya_lc_suspend_enabled,
        #         installs.aya_lc_suspend_switch_callback,
        #     )
        #     self.pack_start(switch_item_aya_lc_suspend, False, False, 0)
