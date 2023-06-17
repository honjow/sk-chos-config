#!/usr/bin/python
# coding=utf-8

import os
import gi
from component import AboutPage, ManagerItem, SwitchItem, UpdateFullButton
import install_utils

from utils import (
    check_decky_plugin_exists,
    check_service_autostart,
    check_service_exists,
    get_product_name,
)

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class SkHoloisoConfigApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            #  application_id="com.honjow.sk-holoiso-config",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.product_name = get_product_name()
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        print("启动Sk Holoiso Config")
        # 创建主窗口
        window = Gtk.ApplicationWindow(application=app)
        window.set_default_size(600, 500)
        window.set_title("Sk SteamOS 配置")

        window.set_icon_name("logisim")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        window.add(scrolled_window)

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        window.set_titlebar(header_bar)

        # 创建垂直布局容器
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        vbox.set_margin_top(10)
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

        # 堆栈切换器和堆栈容器添加
        # header_bar.pack_start(stack_switcher)
        # label = Gtk.Label()
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.pack_start(stack_switcher, False, False, 0)
        # header_box.pack_start(label, True, True, 0)

        header_bar.set_custom_title(header_box)

        # vbox.pack_start(stack_switcher, False, False, 0)
        vbox.pack_start(stack, True, True, 0)

        # 相关功能开关
        switch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        switch_box.set_margin_bottom(10)
        # vbox.pack_start(switch_box, True, True, 0)

        stack.add_titled(switch_box, "switch", "功能开关")

        handycon_enabled = check_service_autostart("handycon.service")
        switch_item_handycon = SwitchItem(
            "HandyGCCS",
            "用来驱动部分掌机的手柄按钮",
            handycon_enabled,
            install_utils.handycon_switch_callback,
        )
        switch_box.pack_start(switch_item_handycon, False, False, 0)

        if self.product_name == "ONEXPLAYER 2 ARP23":
            oxp2lsusb_enabled = check_service_autostart("oxp2-lsusb.service")
            switch_item_oxp2lsusb = SwitchItem(
                "OXP2手柄热插拔检测修复",
                "修复OXP2手柄热插拔后不识别的问题",
                oxp2lsusb_enabled,
                install_utils.oxp2lsusb_switch_callback,
            )
            switch_box.pack_start(switch_item_oxp2lsusb, False, False, 0)

            oxp2_volume_button_fix_enabled = check_service_autostart(
                "oxp2-volume-button-fix.service"
            )
            switch_item_oxp2_volume_button_fix = SwitchItem(
                "OXP2音量键修复",
                "修复OXP2音量键问题",
                oxp2_volume_button_fix_enabled,
                install_utils.oxp2_volume_button_fix_switch_callback,
            )
            switch_box.pack_start(switch_item_oxp2_volume_button_fix, False, False, 0)

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
            aya_lc_suspend_file = "/usr/share/handygccs/aya-lc-suspend"
            aya_lc_suspend_enabled = os.path.isfile(aya_lc_suspend_file)
            switch_item_aya_lc_suspend = SwitchItem(
                "AYANEO LC键睡眠",
                "默认为截图, 开启后LC键作为睡眠键",
                aya_lc_suspend_enabled,
                install_utils.aya_lc_suspend_switch_callback,
            )
            switch_box.pack_start(switch_item_aya_lc_suspend, False, False, 0)

        # 管理
        manager_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        stack.add_titled(manager_page, "manager", "安装管理")

        item_decky = ManagerItem(
            "Decky",
            "游戏模式的插件平台",
            lambda: check_service_exists("plugin_loader.service"),
            install_utils.simple_decky_install,
        )
        manager_page.pack_start(item_decky, False, False, 0)

        item_handycon = ManagerItem(
            "HandyGCCS",
            "驱动部分掌机的手柄按钮",
            lambda: check_service_exists("handycon.service"),
            install_utils.handycon_install,
            install_utils.handycon_uninstall,
        )
        manager_page.pack_start(item_handycon, False, False, 0)

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
                install_utils.ayaled_install,
                lambda: install_utils.remove_decky_plugin("ayaled"),
            )
            manager_page.pack_start(item_ayaled, False, False, 0)

        item_power_control = ManagerItem(
            "PowerControl",
            "掌机功耗性能管理Decky插件",
            lambda: check_decky_plugin_exists("PowerControl"),
            install_utils.power_control_install,
            lambda: install_utils.remove_decky_plugin("PowerControl"),
        )
        manager_page.pack_start(item_power_control, False, False, 0)

        item_tomoon = ManagerItem(
            "ToMoon",
            "科学上网Decky插件",
            lambda: check_decky_plugin_exists("tomoon"),
            install_utils.tomoon_install,
            lambda: install_utils.remove_decky_plugin("tomoon"),
        )
        manager_page.pack_start(item_tomoon, False, False, 0)

        item_this_app = ManagerItem(
            "本程序", "SkHoloisoConfig", True, install_utils.this_app_install
        )
        manager_page.pack_start(item_this_app, False, False, 0)

        # def test_installed():
        #     return True
        # def test_install():
        #     time.sleep(2)
        # def test_uninstall():
        #     time.sleep(2)
        # item_test = ManagerItem("Test", "测试项目", True, test_install, test_uninstall)
        # manager_page.pack_start(item_test, False, False, 0)

        # 关于
        stack.add_titled(AboutPage(), "about", "关于")

        self.loading_spinner = Gtk.Spinner()

        window.show_all()


def main():
    app = SkHoloisoConfigApp()
    app.run(None)


if __name__ == "__main__":
    main()
