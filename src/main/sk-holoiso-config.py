#!/usr/bin/python
# coding=utf-8

import os
import gi
from component import AboutPage, FunctionSwitch, UpdateButton
import update

from utils import check_service_autostart, get_product_name

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class SkHoloisoConfigApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                #  application_id="com.honjow.sk-holoiso-config",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.product_name = get_product_name()
        self.connect("activate", self.on_activate)
    

    def on_activate(self, app):
        print("启动Sk Holoiso Config")
        # 创建主窗口
        window = Gtk.ApplicationWindow(application=app)
        window.set_default_size(600, 460)
        window.set_title("Sk SteamOS 配置")

        window.set_icon_name("logisim")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        window.add(scrolled_window)

        # header_bar = Gtk.HeaderBar()
        # header_bar.set_show_close_button(True)
        # window.set_titlebar(header_bar)

        # 创建垂直布局容器
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        scrolled_window.add(vbox)

        # 创建堆栈容器
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(300)

        # 创建堆栈切换器
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        stack_switcher.set_halign(Gtk.Align.CENTER)
        stack_switcher.set_valign(Gtk.Align.CENTER)

        # 将堆栈切换器和堆栈容器添加到垂直布局容器中
        vbox.pack_start(stack_switcher, False, True, 0)
        vbox.pack_start(stack, True, True, 0)

        # 第一组：相关功能开关
        switch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        switch_box.set_margin_bottom(10)
        # vbox.pack_start(switch_box, True, True, 0)

        # label1 = Gtk.Label()
        # label1.set_markup("<b>功能开关</b>")
        # label1.set_halign(Gtk.Align.START)
        # switch_box.pack_start(label1, False, False, 0)

        stack.add_titled(switch_box, "switch", "功能开关")

        handycon_enabled = check_service_autostart("handycon.service")
        function_switch_handycon = FunctionSwitch("HandyGCCS", "用来驱动部分掌机的手柄按钮", handycon_enabled, update.handycon_switch_callback)
        switch_box.pack_start(function_switch_handycon, False, False, 0)

        if self.product_name == "ONEXPLAYER 2 ARP23":
            oxp2lsusb_enabled = check_service_autostart("oxp2-lsusb.service")
            function_switch_oxp2lsusb = FunctionSwitch("OXP2手柄热插拔检测修复", "修复OXP2手柄热插拔后不识别的问题", oxp2lsusb_enabled, update.oxp2lsusb_switch_callback)
            switch_box.pack_start(function_switch_oxp2lsusb, False, False, 0)

            oxp2_volume_button_fix_enabled = check_service_autostart("oxp2-volume-button-fix.service")
            function_switch_oxp2_volume_button_fix = FunctionSwitch("OXP2音量键修复", "修复OXP2音量键问题", oxp2_volume_button_fix_enabled, update.oxp2_volume_button_fix_switch_callback)
            switch_box.pack_start(function_switch_oxp2_volume_button_fix, False, False, 0)

        if self.product_name in (
            "NEXT",
            "NEXT Pro",
            "NEXT Advance",
            "AYANEO NEXT",
            "AYANEO NEXT Pro",
            "AYANEO NEXT Advance",
            "AIR",
            "AIR Pro",
            "AIR Plus",
            "AYANEO 2",
            "GEEK",
            "AYANEO 2S",
            ):
            aya_lc_suspend_file = '/usr/share/handygccs/aya-lc-suspend'
            aya_lc_suspend_enabled = os.path.isfile(aya_lc_suspend_file)
            # aya_lc_suspend_enabled = False
            function_switch_aya_lc_suspend = FunctionSwitch("AYANEO LC键睡眠", "默认为截图, 开启后LC键作为睡眠键", aya_lc_suspend_enabled, update.aya_lc_suspend_switch_callback)
            switch_box.pack_start(function_switch_aya_lc_suspend, False, False, 0)

        # 第二组：手动更新
        update_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        update_box.set_margin_top(10)
        # vbox.pack_start(update_box, True, True, 0)

        # label2 = Gtk.Label()
        # label2.set_markup("<b>手动更新</b>")
        # label2.set_halign(Gtk.Align.START)
        # update_box.pack_start(label2, False, False, 0)

        stack.add_titled(update_box, "update", "手动更新")

        update_button1 = UpdateButton("更新HandyGCCS", update.handycon_update_callback)
        update_box.pack_start(update_button1, False, False, 0)

        update_button2 = UpdateButton("更新Decky (插件平台)", update.simple_decky_update_callback)
        update_box.pack_start(update_button2, False, False, 0)

        update_pwc = UpdateButton("更新 PowerControl", update.power_control_update_callback)
        update_box.pack_start(update_pwc, False, False, 0)

        update_button_tomoon = UpdateButton("更新Tomoon", update.tomoon_update_callback)
        update_box.pack_start(update_button_tomoon, False, False, 0)

        update_button_this = UpdateButton("更新本程序", update.this_update_callback)
        update_box.pack_start(update_button_this, False, False, 0)

        # 第三组：关于
        stack.add_titled(AboutPage(), "about", "关于")

        self.loading_spinner = Gtk.Spinner()

        window.show_all()


def main():
    app = SkHoloisoConfigApp()
    app.run(None)

if __name__ == "__main__":
    main()