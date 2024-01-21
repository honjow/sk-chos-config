#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import gi
from component import ManagerItem
import installs
import utils


class SoftManagerPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(20)
        self.set_margin_end(20)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.create_page()

    def create_page(self):
        item_emudeck = ManagerItem(
            "EmuDeck",
            "模拟器整合平台",
            lambda: utils.check_emudeck_exists(),
            installs.emudeck_install,
        )
        self.pack_start(item_emudeck, False, False, 0)

        item_nix_ = ManagerItem(
            "Nix",
            "Nix 包管理器, 可以在不可变系统上安装软件, 系统更新不会影响软件",
            lambda: utils.check_nix_exists(),
            installs.nix_install,
            installs.nix_uninstall,
        )
        self.pack_start(item_nix_, False, False, 0)

        # item_noto_fonts_cjk = ManagerItem(
        #     "Noto CJK 字体", "Noto CJK 字体, 因为字体太大不内置到系统中, 可以单独安装, 不受系统更新影响", 
        #     lambda: utils.user_noto_fonts_cjk_exists(),
        #     installs.noto_fonts_cjk_install,
        #     installs.noto_fonts_cjk_uninstall,
        # )
        # self.pack_start(item_noto_fonts_cjk, False, False, 0)

        item_this_app = ManagerItem(
            "本程序", "Sk ChimeraOS Tool", True, installs.this_app_install
        )
        self.pack_start(item_this_app, False, False, 0)

        item_this_app_cn = ManagerItem(
            "本程序(备用国内地址)", "Sk ChimeraOS Tool", True, installs.this_app_cn_install
        )
        self.pack_start(item_this_app_cn, False, False, 0)