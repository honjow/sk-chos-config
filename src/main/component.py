#!/usr/bin/python
# coding=utf-8

import gi
gi.require_version("Gtk", "3.0")
import threading
from gi.repository import GLib, Gtk, Pango


class FunctionSwitch(Gtk.Box):
    def __init__(self, function_name, description, initial_value=False, callback=None):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        # self.set_margin_start(20)
        # self.set_margin_end(20)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

        self.callback = callback
        self.last_value = initial_value

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
        switch.props.height_request = 46
        switch.props.width_request = 100
        switch.connect("notify::active", self.on_switch_activated)
        switch.set_active(initial_value)
        switch_box = Gtk.Box()
        switch_box.set_margin_start(10)
        switch_box.set_valign(Gtk.Align.CENTER)
        switch_box.pack_start(switch, False, False, 0)
        self.pack_end(switch_box, False, False, 0)

    def on_switch_activated(self, switch, gparam):
        active = switch.get_active()
        if self.callback and active != self.last_value:
            self.callback(active)
            self.last_value = active

class UpdateButton(Gtk.Button):
    def __init__(self, function_name, callback=None):
        Gtk.Button.__init__(self, label=function_name)

        # self.set_margin_start(20)
        # self.set_margin_end(20)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

        self.set_sensitive(True)

        self.function_name = function_name
        self.callback = callback

        self.connect("clicked", self.on_update_clicked)

    def on_update_clicked(self, button):
        self.set_sensitive(False)
        self.set_label("更新中...")

        # 在一个新线程中执行回调函数
        threading.Thread(target=self.execute_callback).start()

    def execute_callback(self):
        # 执行回调函数，例如模拟耗时操作
        if self.callback:
            result, ret_msg = self.callback()

        # 在主循环中使用 GLib.idle_add() 调用回调函数
        GLib.idle_add(self.update_complete, result, ret_msg)

    def update_complete(self, result, ret_msg=None):
        # 更新完成后恢复按钮状态和文本
        self.set_sensitive(True)
        self.set_label(self.function_name)

        # 根据回调函数的运行结果显示对话框内容
        if result:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=ret_msg if ret_msg else "更新成功",
            )
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=ret_msg,
            )

        dialog.run()
        dialog.destroy()

        return False

