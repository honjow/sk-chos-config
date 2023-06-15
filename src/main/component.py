#!/usr/bin/python
# coding=utf-8

import gi
import threading

gi.require_version("Gtk", "3.0")
import threading
from gi.repository import GLib, Gtk, Pango, Gdk


class FunctionSwitch(Gtk.Box):
    def __init__(self, title, description, initial_value=False, callback=None):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

        self.callback = callback
        self.last_value = initial_value

        # 左边文字部分
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.pack_start(left_box, True, True, 0)

        switch_label = Gtk.Label()
        switch_label.set_text(title)
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
        # switch.set_size_request(80, 40)
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
    def __init__(self, title, callback=None):
        Gtk.Button.__init__(self, label=title)

        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

        self.set_sensitive(True)

        self.function_name = title
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

class AboutPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(20)
        self.set_margin_end(20)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.create_page()
    
    def open_website(label, uri):
        Gdk.spawn_command_line_async(f'xdg-open {uri}')

    def create_page(self):

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_margin_top(20)
        grid.set_margin_bottom(20)
        grid.set_margin_start(20)
        grid.set_margin_end(20)
        grid.set_halign(Gtk.Align.CENTER)

        # 应用程序名称
        name_label = Gtk.Label()
        name_label.set_text("Sk SteamOS (Holoiso) Config")
        name_label.set_halign(Gtk.Align.CENTER)
        name_label.set_valign(Gtk.Align.CENTER)
        name_label.set_hexpand(True)
        name_label.set_vexpand(True)
        name_label.set_margin_bottom(10)
        name_label.set_margin_top(10)
        name_label.set_margin_start(10)
        name_label.set_margin_end(10)
        name_label.set_markup("<span font_weight='bold' font_size='large'>{}</span>".format(name_label.get_text()))

        # 版本号
        version_label = Gtk.Label()
        version_label.set_text("版本 1.0")
        version_label.set_halign(Gtk.Align.CENTER)
        version_label.set_valign(Gtk.Align.CENTER)

        # 作者
        authors_label = Gtk.Label()
        authors_label.set_text("作者: Honjow")
        authors_label.set_halign(Gtk.Align.CENTER)
        authors_label.set_valign(Gtk.Align.CENTER)

        # 官方网站
        website_label = Gtk.Label()
        url = "https://github.com/honjow/sk-holoiso-config"
        website_label.set_markup(f"Github: <a href='{url}'>{url}</a>")
        website_label.set_halign(Gtk.Align.CENTER)
        website_label.set_valign(Gtk.Align.CENTER)
        website_label.set_use_markup(True)
        website_label.connect("activate-link", self.open_website, url)
        # website_label.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        # 设置部件在网格中的位置
        grid.attach(name_label, 0, 0, 2, 1)
        grid.attach(version_label, 0, 1, 2, 1)
        grid.attach(authors_label, 0, 2, 2, 1)
        grid.attach(website_label, 0, 3, 2, 1)

        self.pack_start(grid, True, True, 0)