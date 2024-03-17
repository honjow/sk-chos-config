#!/usr/bin/python
# coding=utf-8


import gi
from pages.advance import AdvancePage
from pages.switch import SwitchPage
from pages.tool import ToolManagerPage
from pages.soft import SoftManagerPage
from pages.about import AboutPage
from pages.autoupt_switch import AutoUpdateSwitchPage
from pages.decky import DeckyManagerPage
from pages.decky_advande import DeckyAdvanceManagerPage
import utils
from config import logging

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class ContentView(Gtk.Box):
    def __init__(self, category):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # 在这里添加每个选项的具体布局
        label = Gtk.Label(label=f"内容布局 {category}")
        self.pack_start(label, True, True, 0)


class CategoryRow(Gtk.ListBoxRow):
    def __init__(self, category, activate_callback):
        Gtk.ListBoxRow.__init__(self)
        self.activate_callback = activate_callback
        self.category = category

        event_box = Gtk.EventBox()
        event_box.connect("button-press-event", self.on_button_press)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        label = Gtk.Label(label=category)
        box.add(label)
        event_box.add(box)
        self.add(event_box)

    def on_button_press(self, widget, event):
        # 调用外部传递的回调函数
        if self.activate_callback:
            self.activate_callback(widget, self.category)


class PanedScrolledWindow(Gtk.ScrolledWindow):
    def __init__(self, box: Gtk.Box):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add(box)


class ColumnedWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, application=app, title="Sk ChimeraOS 配置")
        self.set_default_size(800, 500)

        # 检查必须依赖
        utils.check_and_install_addon()

        self.box_mapping = {
            "功能开关": SwitchPage(),
            "工具": ToolManagerPage(),
            "Decky 插件": DeckyManagerPage(),
            # "Decky 高级": DeckyAdvanceManagerPage(),
            "软件&游戏": SoftManagerPage(),
            "高级": AdvancePage(),
            "自动更新": AutoUpdateSwitchPage(),
            "关于": AboutPage(),
        }
        self.scrolled_window_mapping = {}
        for category, box in self.box_mapping.items():
            self.scrolled_window_mapping[category] = PanedScrolledWindow(box)

        # 创建一个垂直布局
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(main_box)

        # 创建一个水平布局用于左右分栏
        paned = Gtk.Paned()
        main_box.pack_start(paned, True, True, 0)

        # 左边栏
        left_panel = Gtk.ListBox()
        left_panel.set_size_request(180, -1)  # 设置左边栏的宽度
        paned.pack1(left_panel, False, False)

        # 添加左边栏中的分类项
        categories = list(self.scrolled_window_mapping.keys())
        for category in categories:
            row = CategoryRow(category, self.on_category_clicked)
            left_panel.add(row)

        # 右边栏
        self.right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        paned.pack2(self.right_panel, True, True)

        # 默认显示第一项的内容
        self.current_content = None
        self.on_category_clicked(None, categories[0])

    def on_category_clicked(self, widget, category):
        # 移除之前显示的内容
        if self.current_content:
            self.right_panel.remove(self.current_content)

        # 使用字典中的对应关系获取对应的 Box 类
        content_view = self.scrolled_window_mapping[category]

        # 如果存在则添加到右栏中
        if content_view:
            self.right_panel.pack_start(content_view, True, True, 0)
            self.current_content = content_view

            # 确保所有子组件都被显示
            self.right_panel.show_all()


class SkHoloisoConfigApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            #  application_id="com.honjow.sk-holoiso-config",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        logging.info("启动Sk chirmeaos Tool New")

        utils.run_command("sudo frzr-unlock")

        win = ColumnedWindow(self)
        win.show_all()


def main():
    app = SkHoloisoConfigApp()
    app.run(None)


if __name__ == "__main__":
    main()
