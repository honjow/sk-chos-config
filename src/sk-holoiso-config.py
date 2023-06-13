#!/usr/bin/python
# coding=utf-8
import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Gio, Pango


class FunctionSwitch(Gtk.Box):
    def __init__(self, function_name, description, initial_value=False):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.set_margin_start(20)
        self.set_margin_end(20)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

        # 左边文字部分
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.pack_start(left_box, True, True, 0)

        switch_label = Gtk.Label()
        switch_label.set_text(function_name)
        switch_label.set_halign(Gtk.Align.START)
        switch_label.set_valign(Gtk.Align.START)
        left_box.pack_start(switch_label, False, False, 0)

        desc_label = Gtk.Label()
        desc_label.set_text(description)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_valign(Gtk.Align.START)
        desc_label.set_xalign(0)
        desc_label.set_yalign(0)
        desc_label.set_line_wrap(True)
        desc_label.set_line_wrap_mode(Pango.WrapMode.WORD)
        desc_label.set_ellipsize(Pango.EllipsizeMode.NONE)
        desc_label.set_markup("<small>" + desc_label.get_text() + "</small>")
        left_box.pack_start(desc_label, False, False, 0)

        # 右边开关部分
        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        switch.connect("notify::active", self.on_switch_activated, function_name)
        switch.set_active(initial_value)
        switch_box = Gtk.Box()
        switch_box.set_margin_start(10)
        switch_box.set_valign(Gtk.Align.CENTER)
        switch_box.pack_start(switch, False, False, 0)
        self.pack_end(switch_box, False, False, 0)

    def on_switch_activated(self, switch, gparam, function_name):
        state = switch.get_active()
        if state:
            print(f"{function_name} 开关已打开")
        else:
            print(f"{function_name} 开关已关闭")

class UpdateButton(Gtk.Button):
    def __init__(self, function_name):
        Gtk.Button.__init__(self, label=function_name)

        self.set_margin_start(20)
        self.set_margin_end(20)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

        self.set_sensitive(True)

        self.function_name = function_name

        self.connect("clicked", self.on_update_clicked)

    def on_update_clicked(self, button):
        # 模拟更新过程，延迟2秒钟
        GLib.timeout_add_seconds(2, self.update_complete)

        self.set_sensitive(False)
        self.set_label("更新中...")

    def update_complete(self):
        # 更新完成后恢复按钮状态和文本
        self.set_sensitive(True)
        self.set_label(self.function_name)
        return False

class SkHoloisoConfigApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="com.honjow.skholoisoconfig",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.on_activate)
    

    def on_activate(self, app):
        # 创建主窗口
        window = Gtk.ApplicationWindow(application=app)
        window.set_default_size(500, 420)
        window.set_title("Sk SteamOS 配置")

        window.set_icon_name("logisim")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        window.add(scrolled_window)

        # 创建垂直布局容器
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        scrolled_window.add(vbox)

        # 第一组：相关功能开关
        group1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(group1, True, True, 0)

        label1 = Gtk.Label()
        label1.set_markup("<b>功能开关</b>")
        group1.pack_start(label1, False, False, 0)

        function_witch1 = FunctionSwitch("HandyGCCS", "用来驱动部分掌机的手柄按钮", initial_value=True)
        group1.pack_start(function_witch1, False, False, 0)

        function_witch2 = FunctionSwitch("功能2", "功能2的说明功能用来驱动部分掌机的手柄按钮用来驱动部分掌机的手柄按钮")
        group1.pack_start(function_witch2, False, False, 0)

        # # 第二组：手动更新
        group2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.pack_start(group2, True, True, 0)

        label2 = Gtk.Label()
        label2.set_markup("<b>手动更新</b>")
        group2.pack_start(label2, False, False, 0)

        update_button1 = UpdateButton("更新HandyGCCS")
        group2.pack_start(update_button1, False, False, 0)

        update_button2 = UpdateButton("更新功能2")
        group2.pack_start(update_button2, False, False, 0)

        self.loading_spinner = Gtk.Spinner()

        window.show_all()

    def on_update_button_clicked(self, button, function_name):
        self.loading_spinner.start()
        print(f"正在更新 {function_name}...")
        # 模拟长时间操作
        GLib.timeout_add_seconds(3, self.finish_update, function_name)

    def finish_update(self, function_name):
        self.loading_spinner.stop()
        print(f"{function_name} 更新完成")

app = SkHoloisoConfigApp()
app.run(None)