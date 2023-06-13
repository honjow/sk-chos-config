#!/usr/bin/python
# coding=utf-8
import os
import sys
import gi
import threading
import time
import urllib.request
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Gio, Pango

def get_product_name():
    # get from /sys/devices/virtual/dmi/id/product_name
    product_name = ""
    try:
        with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
            product_name = f.readline().strip()
    except Exception as e:
        print("读取设备名称失败:", str(e))
    return product_name


def handycon_switch_callback(active):
    toggle_service("handycon.service", active)

def oxp2lsusb_switch_callback(active):
    toggle_service("oxp2-lsusb.service", active)

def oxp2_volume_button_fix_switch_callback(active):
    toggle_service("oxp2-volume-button-fix.service", active)

def handycon_update_callback():
    print("执行 HandyGCCS 更新操作")
    # 判断 ~/.cache/sk-holoiso-config/git/HandyGCCS 是否存在
    git_directory = os.path.expanduser("~/.cache/sk-holoiso-config/git/HandyGCCS")
    if os.path.exists(git_directory):
        print("更新git目录并执行更新")
        command = "cd {} && git pull && sudo make install".format(git_directory)
    else:
        print("新建git目录并执行更新")
        command = "mkdir -p ~/.cache/sk-holoiso-config/git && git clone https://github.com/honjow/HandyGCCS.git {} && sudo make install".format(git_directory)

    return run_command(command, "HandyGCCS")


def decky_update_callback():
    success = True
    ret_msg = None
    print("执行Decky更新操作")
    
    # 判断 ~/.cache/sk-holoiso-config/user_install_script.sh 是否存在
    script_path = os.path.expanduser("~/.cache/sk-holoiso-config/user_install_script.sh")
    if os.path.exists(script_path):
        # 删除已存在的脚本文件
        os.remove(script_path)
    # 下载最新的脚本文件
    script_url = "https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/user_install_script.sh"
    try:
        urllib.request.urlretrieve(script_url, script_path)
        print("脚本文件下载完成")
    except Exception as e:
        print("下载脚本文件时出现错误:", str(e))
        success = False
        ret_msg = str(e)
        return success, ret_msg
    # 给脚本文件添加执行权限
    os.chmod(script_path, 0o755)
    # 在bash中执行脚本文件
    os.system("sudo sh {}".format(script_path))
    print("Decky更新完成")
    return success, ret_msg

def simple_decky_update_callback():
    command = "curl -Lk https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh | sed 's#prerelease == \"false\"#prerelease == \"true\"#' | sudo sh"
    return run_command(command, "Decky")

def tomoon_update_callback():
    command = "curl -L http://i.ohmydeck.net | sh"
    # command = "ls /abcd"
    return run_command(command, "ToMoon")

def this_update_callback():
    command = "yay -Sy sk-holoiso-config --noconfirm --overwrite \"*\""
    success, ret_msg = run_command(command, "Sk Holoiso Config")
    if success:
        ret_msg = "更新完成, 请重新启动应用"
    return success, ret_msg
    

# 执行命令
def run_command(command, name=""):
    success = True
    ret_msg = ""
    print(f"执行{name}更新操作")
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in process.stdout:
            print(line.strip())
        stdout, stderr = process.communicate()
        return_code = process.returncode

        if return_code != 0:
            success = False
            ret_msg = stderr.decode().strip()
            print(f"{name}更新失败: {ret_msg}")
        else:
            print(f"{name}更新完成")
    except Exception as e:
        success = False
        ret_msg = str(e)
        print(f"{name}更新失败: {ret_msg}")
    
    return success, ret_msg

# 检查服务是否已启用
def check_service_autostart(service_name):
    try:
        output = subprocess.check_output(['sudo', 'systemctl', 'is-enabled', service_name]).decode().strip()
        return output == 'enabled'
    except subprocess.CalledProcessError:
        # 如果命令执行出错，则服务可能不存在或无法访问
        return False

def toggle_service(service_name, enable):
    action = "enable" if enable else "disable"
    try:
        sudo_cmd = ['sudo', 'systemctl', action, '--now', service_name]
        subprocess.run(sudo_cmd, check=True)
        print(f"服务 {service_name} {action}成功")
    except subprocess.CalledProcessError as e:
        print(f"服务 {service_name} {action}失败:", str(e))


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

        update_button1 = UpdateButton("更新HandyGCCS", handycon_update_callback)
        group2.pack_start(update_button1, False, False, 0)

        update_button2 = UpdateButton("更新Decky (插件平台)", simple_decky_update_callback)
        group2.pack_start(update_button2, False, False, 0)

        update_button_tomoon = UpdateButton("更新Tomoon", tomoon_update_callback)
        group2.pack_start(update_button_tomoon, False, False, 0)

        update_button_this = UpdateButton("更新本程序", this_update_callback)
        group2.pack_start(update_button_this, False, False, 0)

        self.loading_spinner = Gtk.Spinner()

        window.show_all()


app = SkHoloisoConfigApp()
app.run(None)