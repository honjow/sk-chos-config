#!/usr/bin/python
# coding=utf-8

import os
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
)

class SoftManagerPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.create_page()

    def create_page(self):
        item_emudeck = ManagerItem(
            "EmuDeck",
            "模拟器整合平台",
            lambda: utils.check_emudeck_exists(),
            installs.emudeck_install,
        )
        self.pack_start(item_emudeck, False, False, 0)

        item_anime_games_launcher = ManagerItem(
            "Anime Games Launcher",
            "动漫游戏启动器 (米哈游全家桶)",
            lambda: os.path.isfile(os.path.expanduser("~/Applications/anime-games-launcher.AppImage")),
            installs.anime_games_launcher_install,
        )
        self.pack_start(item_anime_games_launcher, False, False, 0)

        item_an_anime_games_launcher = ManagerItem(
            "An Anime Games Launcher",
            "动漫游戏启动器 (原神)",
            lambda: os.path.isfile(os.path.expanduser("~/Applications/an-anime-games-launcher.AppImage")),
            installs.an_anime_games_launcher_install,
        )

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