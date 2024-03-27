#!/usr/bin/python
# coding=utf-8

import gi
import threading

gi.require_version("Gtk", "3.0")
import threading
from gi.repository import GLib, Gtk, Pango

from config import logging


class SwitchItem(Gtk.Box):
    def __init__(
        self,
        title,
        description="",
        initial_value=False,
        callback=None,
        turnOnCallback=None,
        turnOffCallback=None,
    ):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.set_margin_start(2)
        self.set_margin_end(2)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

        self.callback = callback
        self.last_value = initial_value
        self.turnOnCallback = turnOnCallback
        self.turnOffCallback = turnOffCallback

        # 左边文字部分
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.pack_start(left_box, True, True, 0)

        self.switch_label = Gtk.Label()
        self.switch_label.set_text(title)
        self.switch_label.set_halign(Gtk.Align.START)
        self.switch_label.set_valign(Gtk.Align.START)
        left_box.pack_start(self.switch_label, False, False, 0)

        self.desc_label = Gtk.Label()
        self.desc_label.set_text(description)
        self.desc_label.set_halign(Gtk.Align.START)
        self.desc_label.set_valign(Gtk.Align.START)
        self.desc_label.set_xalign(0)
        self.desc_label.set_yalign(0)
        self.desc_label.set_line_wrap(True)
        self.desc_label.set_line_wrap_mode(Pango.WrapMode.WORD)
        self.desc_label.set_ellipsize(Pango.EllipsizeMode.NONE)
        self.desc_label.set_markup("<small>" + self.desc_label.get_text() + "</small>")
        if description and description != "":
            left_box.pack_start(self.desc_label, False, False, 0)

        # 右边开关部分
        self.switch = Gtk.Switch()
        self.switch.props.valign = Gtk.Align.CENTER
        # self.switch.set_size_request(80, 40)
        self.switch.connect("notify::active", self.on_switch_activated)
        self.switch.set_active(initial_value)
        switch_box = Gtk.Box()
        switch_box.set_margin_start(10)
        switch_box.set_valign(Gtk.Align.CENTER)
        switch_box.pack_start(self.switch, False, False, 0)
        self.pack_end(switch_box, False, False, 0)

    def on_switch_activated(self, switch, gparam):
        active = switch.get_active()
        if self.callback and active != self.last_value:
            self.callback(active)
            self.last_value = active
            if active:
                if callable(self.turnOnCallback):
                    self.turnOnCallback()
            else:
                if callable(self.turnOffCallback):
                    self.turnOffCallback()

    def set_value(self, value):
        self.switch.set_active(value)


class ManagerItem(Gtk.Box):
    def __init__(
        self,
        title,
        description,
        installed_cb,
        install_callback=None,
        uninstall_callback=None,
        version_cb=None,
        latest_version_cb=None,
    ):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.set_margin_start(2)
        self.set_margin_end(2)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

        self.title = title
        self.install_callback = install_callback
        self.uninstall_callback = uninstall_callback
        self.install_button = None
        self.uninstall_button = None
        self.version_cb = version_cb
        self.latest_version_cb = latest_version_cb

        # 创建按钮时不显示
        self.uninstall_button_visible = False
        self.install_button_visible = True

        self.installed_cb = installed_cb

        if callable(self.installed_cb):
            self.current_installed = self.installed_cb()
        else:
            self.current_installed = self.installed_cb
        
        if callable(version_cb):
            self.current_version = self.version_cb()
        else:
            self.current_version = self.version_cb
        
        if callable(latest_version_cb):
            self.latest_version = self.latest_version_cb()
        else:
            self.latest_version = self.latest_version_cb

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

        # 版本信息
        version_Box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.pack_start(version_Box, True, True, 0)
        if self.current_version:
            version_label = Gtk.Label()
            version_label.set_text("当前: " + self.current_version)
            version_label.set_halign(Gtk.Align.START)
            version_label.set_valign(Gtk.Align.START)
            version_Box.pack_start(version_label, False, False, 0)
        if self.latest_version:
            latest_version_label = Gtk.Label()
            latest_version_label.set_text("最新: " + self.latest_version)
            latest_version_label.set_halign(Gtk.Align.START)
            latest_version_label.set_valign(Gtk.Align.START)
            version_Box.pack_start(latest_version_label, False, False, 0)

        # 加载动画部分
        self.spinner = Gtk.Spinner()
        self.spinner.set_valign(Gtk.Align.CENTER)
        self.spinner.set_margin_end(10)
        self.pack_start(self.spinner, False, False, 0)

        # 右边按钮部分
        if self.uninstall_callback is not None:
            self.uninstall_button = Gtk.Button()
            self.uninstall_button.set_margin_end(10)
            self.uninstall_button.set_label("卸载")
            self.uninstall_button.set_valign(Gtk.Align.CENTER)
            self.uninstall_button.connect("clicked", self.on_uninstall_clicked)
            self.pack_start(self.uninstall_button, False, False, 0)
            if not self.current_installed:
                GLib.idle_add(self.uninstall_button.hide)

        if self.install_callback is not None:
            self.install_button = Gtk.Button()
            self.install_button.set_label("更新" if self.current_installed else "安装")
            self.install_button.set_valign(Gtk.Align.CENTER)
            self.install_button.connect("clicked", self.on_install_clicked)
            self.pack_start(self.install_button, False, False, 0)

        GLib.idle_add(self.check_and_update_visibility)

        # 定期检查条件并更新按钮的可见性
        # GLib.timeout_add(1000, self.check_and_update_visibility)

    def check_and_update_visibility(self):
        # 根据条件设置按钮的可见性
        if self.current_installed:
            self.uninstall_button_visible = True
        else:
            self.uninstall_button_visible = False

        self.update_install_button()
        # 更新按钮的可见性
        self.update_buttons_visibility()

        # 返回 True 继续定期检查，返回 False 停止检查
        return True

    def disable_buttons(self):
        if self.install_button is not None:
            self.install_button.set_sensitive(False)
        if self.uninstall_button is not None:
            self.uninstall_button.set_sensitive(False)
        self.spinner.start()

    def enable_buttons(self):
        if self.install_button is not None:
            self.install_button.set_sensitive(True)
        if self.uninstall_button is not None:
            self.uninstall_button.set_sensitive(True)
        self.spinner.stop()

    def reload_installed(self):
        if callable(self.installed_cb):
            self.current_installed = self.installed_cb()
        else:
            self.current_installed = self.installed_cb

        if self.current_installed:
            self.uninstall_button_visible = True
        else:
            self.uninstall_button_visible = False

        # 更新按钮的可见性
        GLib.idle_add(self.update_install_button)
        GLib.idle_add(self.update_buttons_visibility)

    def update_buttons_visibility(self):
        # 根据条件设置按钮的可见性
        if self.install_button is not None:
            self.install_button.set_visible(self.install_button_visible)
        if self.uninstall_button is not None:
            self.uninstall_button.set_visible(self.uninstall_button_visible)

    def update_install_button(self):
        if self.install_button is not None:
            if self.current_installed:
                self.install_button.set_label("更新")
            else:
                self.install_button.set_label("安装")

    def completed(self, success, install=True, msg=None):
        self.reload_installed()
        self.enable_buttons()
        logging.info(
            "Completed: success: {}, install: {}, msg: {}".format(success, install, msg)
        )
        # 根据回调函数的运行结果显示对话框内容
        if success:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=(
                    msg
                    if msg
                    else "{} {}成功".format(self.title, "安装" if install else "卸载")
                ),
            )
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=msg,
            )

        # 更新按钮的可见性
        GLib.idle_add(self.update_buttons_visibility)
        self.check_and_update_visibility()

        dialog.run()
        dialog.destroy()

    def execute_callback(self, callback, install):
        success, ret_msg = callback()
        GLib.idle_add(self.completed, success, install, ret_msg)

    def on_install_clicked(self, button):
        self.disable_buttons()
        threading.Thread(
            target=self.execute_callback, args=(self.install_callback, True)
        ).start()

    def on_uninstall_clicked(self, button):
        self.disable_buttons()
        threading.Thread(
            target=self.execute_callback, args=(self.uninstall_callback, False)
        ).start()


class AsyncActionFullButton(Gtk.Box):
    def __init__(self, title, description=None, callback=None):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.set_margin_start(2)
        self.set_margin_end(2)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

        self.function_name = title
        self.callback = callback

        self.button = Gtk.Button()
        self.button.set_label(title)
        self.button.set_margin_start(5)
        self.button.set_margin_end(5)
        self.button.set_margin_top(5)
        self.button.set_margin_bottom(5)
        self.button.set_sensitive(True)
        self.button.connect("clicked", self.on_clicked)

        self.pack_start(self.button, True, True, 0)

        if description:
            desc_label = Gtk.Label()
            desc_label.set_text(description)
            desc_label.set_halign(Gtk.Align.CENTER)
            desc_label.set_valign(Gtk.Align.START)
            desc_label.set_xalign(0)
            desc_label.set_yalign(0)
            desc_label.set_line_wrap(True)
            desc_label.set_line_wrap_mode(Pango.WrapMode.WORD)
            desc_label.set_ellipsize(Pango.EllipsizeMode.NONE)
            desc_label.set_markup("<small>" + desc_label.get_text() + "</small>")
            self.pack_start(desc_label, False, False, 0)

    def on_clicked(self, button):
        self.button.set_sensitive(False)
        self.button.set_label("处理中...")

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
        self.button.set_label(self.function_name)

        # 根据回调函数的运行结果显示对话框内容
        if result:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=ret_msg if ret_msg else "处理成功",
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
