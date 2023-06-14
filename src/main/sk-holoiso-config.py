#!/usr/bin/python
# coding=utf-8

import gi
from component import FunctionSwitch, UpdateButton
import update

from utils import check_service_autostart, get_product_name, toggle_service

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


def handycon_switch_callback(active):
    toggle_service("handycon.service", active)

def oxp2lsusb_switch_callback(active):
    toggle_service("oxp2-lsusb.service", active)

def oxp2_volume_button_fix_switch_callback(active):
    toggle_service("oxp2-volume-button-fix.service", active)



class SkHoloisoConfigApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="com.honjow.skholoisoconfig",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.product_name = get_product_name()
        self.connect("activate", self.on_activate)
    

    def on_activate(self, app):
        # 创建主窗口
        window = Gtk.ApplicationWindow(application=app)
        window.set_default_size(500, 620)
        window.set_title("Sk SteamOS 配置")

        window.set_icon_name("logisim")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        window.add(scrolled_window)

        # 创建垂直布局容器
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        scrolled_window.add(vbox)

        # 第一组：相关功能开关
        group1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        group1.set_margin_bottom(10)
        vbox.pack_start(group1, True, True, 0)

        label1 = Gtk.Label()
        label1.set_markup("<b>功能开关</b>")
        label1.set_halign(Gtk.Align.START)
        group1.pack_start(label1, False, False, 0)

        handycon_enabled = check_service_autostart("handycon.service")
        function_switch_handycon = FunctionSwitch("HandyGCCS", "用来驱动部分掌机的手柄按钮", handycon_enabled, handycon_switch_callback)
        group1.pack_start(function_switch_handycon, False, False, 0)

        if self.product_name == "ONEXPLAYER 2 ARP23":
            oxp2lsusb_enabled = check_service_autostart("oxp2-lsusb.service")
            function_switch_oxp2lsusb = FunctionSwitch("OXP2手柄热插拔检测修复", "修复OXP2手柄热插拔后不识别的问题", oxp2lsusb_enabled, oxp2lsusb_switch_callback)
            group1.pack_start(function_switch_oxp2lsusb, False, False, 0)

            oxp2_volume_button_fix_enabled = check_service_autostart("oxp2-volume-button-fix.service")
            function_switch_oxp2_volume_button_fix = FunctionSwitch("OXP2音量键修复", "修复OXP2音量键问题", oxp2_volume_button_fix_enabled, oxp2_volume_button_fix_switch_callback)
            group1.pack_start(function_switch_oxp2_volume_button_fix, False, False, 0)

        # 第二组：手动更新
        group2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.pack_start(group2, True, True, 0)

        label2 = Gtk.Label()
        label2.set_markup("<b>手动更新</b>")
        label2.set_halign(Gtk.Align.START)
        group2.pack_start(label2, False, False, 0)

        update_button1 = UpdateButton("更新HandyGCCS", update.handycon_update_callback)
        group2.pack_start(update_button1, False, False, 0)

        update_button2 = UpdateButton("更新Decky (插件平台)", update.simple_decky_update_callback)
        group2.pack_start(update_button2, False, False, 0)

        update_button_tomoon = UpdateButton("更新Tomoon", update.tomoon_update_callback)
        group2.pack_start(update_button_tomoon, False, False, 0)

        update_button_this = UpdateButton("更新本程序", update.this_update_callback)
        group2.pack_start(update_button_this, False, False, 0)

        self.loading_spinner = Gtk.Spinner()

        window.show_all()


def main():
    app = SkHoloisoConfigApp()
    app.run(None)

if __name__ == "__main__":
    main()