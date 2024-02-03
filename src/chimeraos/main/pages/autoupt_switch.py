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
from utils import check_service_autostart,get_autoupdate,set_autoupdate

from config import (
    IS_HHD_SUPPORT,
    PANED_RIGHT_MARGIN_START,
    PANED_RIGHT_MARGIN_END,
    PANED_RIGHT_MARGIN_TOP,
    PANED_RIGHT_MARGIN_BOTTOM,
    USER,
)

from config import PRODUCT_NAME, logging

class AutoUpdateSwitchPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.product_name = PRODUCT_NAME
        self.create_page()

    def create_page(self):

        auto_update_enabled = check_service_autostart("sk-chos-tool-autoupdate.timer")
        switch_item_auto_update = SwitchItem(
            "自动更新总开关",
            "只有在开启后，下面的开关才会生效",
            auto_update_enabled,
            installs.auto_update_switch_callback,
        )
        self.pack_start(switch_item_auto_update, False, False, 0)

        # sk-chos-tool 本身的自动更新开关
        skt_key = "sk_chos_tool"
        skt_update_enabled = get_autoupdate(skt_key)
        switch_item_skt_update = SwitchItem(
            "自动更新本软件",
            "",
            skt_update_enabled,
            lambda enabled: set_autoupdate(skt_key, enabled),
        )
        self.pack_start(switch_item_skt_update, False, False, 0)

        # HandyGCCS 的自动更新开关
        handy_key = "handygccs"
        handy_update_enabled = get_autoupdate(handy_key)
        switch_item_handy_update = SwitchItem(
            "自动更新 HandyGCCS",
            "",
            handy_update_enabled,
            lambda enabled: set_autoupdate(handy_key, enabled),
        )
        self.pack_start(switch_item_handy_update, False, False, 0)

        # hhd 的自动更新开关
        if IS_HHD_SUPPORT:
            hhd_key = "hhd"
            hhd_update_enabled = get_autoupdate(hhd_key)
            switch_item_hhd_update = SwitchItem(
                "自动更新 HHD",
                "",
                hhd_update_enabled,
                lambda enabled: set_autoupdate(hhd_key, enabled),
            )
            self.pack_start(switch_item_hhd_update, False, False, 0)
        
