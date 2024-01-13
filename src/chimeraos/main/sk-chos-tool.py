#!/usr/bin/python
# coding=utf-8

import gi
from pages.advance import AdvancePage
from pages.switch import SwitchPage
from pages.tool import ToolManagerPage
from pages.soft import SoftManagerPage
from pages.about import AboutPage
import utils
from config import logging


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class SkHoloisoConfigApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            #  application_id="com.honjow.sk-holoiso-config",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        logging.info("启动Sk chirmeaos Tool")

        utils.run_command("sudo frzr-unlock")

        # 创建主窗口
        window = Gtk.ApplicationWindow(application=app)
        window.set_default_size(600, 500)
        window.set_title("Sk ChimeraOS 配置")

        # window.set_icon_name("logisim")
        window.set_icon_name("sk-chos-tool")

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

        # 开关
        stack.add_titled(SwitchPage(), "switch", "功能开关")

        # 工具管理
        stack.add_titled(ToolManagerPage(), "tool", "工具")

        # 软件和游戏
        stack.add_titled(SoftManagerPage(), "soft", "软件&游戏")

        # 高级
        stack.add_titled(AdvancePage(), "advance", "高级")

        # 关于
        stack.add_titled(AboutPage(), "about", "关于")

        self.loading_spinner = Gtk.Spinner()

        window.show_all()


def main():
    app = SkHoloisoConfigApp()
    app.run(None)


if __name__ == "__main__":
    main()
