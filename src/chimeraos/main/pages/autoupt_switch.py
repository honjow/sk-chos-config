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
            "自动更新本软件",
            "开启后会自动检查更新，建议开启",
            auto_update_enabled,
            installs.auto_update_switch_callback,
        )
        self.pack_start(switch_item_auto_update, False, False, 0)
        
