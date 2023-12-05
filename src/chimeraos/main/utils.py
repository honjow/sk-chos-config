#!/usr/bin/python
# coding=utf-8

import configparser
import os
import subprocess

SK_TOOL_PATH = "/usr/share/sk-chos-tool"

def get_product_name():
    # get from /sys/devices/virtual/dmi/id/product_name
    product_name = ""
    try:
        with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
            product_name = f.readline().strip()
    except Exception as e:
        print("读取设备名称失败:", str(e))
    print("设备名称:", product_name)
    return product_name

# 执行命令
def run_command(command, name=""):
    success = True
    ret_msg = ""
    print(f"执行{name}操作")
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in process.stdout:
            print(line.strip())
        stdout, stderr = process.communicate()
        return_code = process.returncode

        if return_code != 0:
            success = False
            ret_msg = stderr.strip()
            print(f"{name}操作失败: {ret_msg}")
        else:
            print(f"{name}操作完成")
    except Exception as e:
        success = False
        ret_msg = str(e)
        print(f"{name}操作失败: {ret_msg}")
    
    return success, ret_msg

# 检查服务是否已启用
def check_service_autostart(service_name):
    try:
        output = subprocess.check_output(['sudo', 'systemctl', 'is-enabled', service_name]).decode().strip()
        return output == 'enabled'
    except subprocess.CalledProcessError:
        # 如果命令执行出错，则服务可能不存在或无法访问
        return False

# 检查服务
def check_service_exists(service_name):
    try:
        # 使用`systemctl is-active`命令检查服务状态
        subprocess.run(['systemctl', 'is-active', service_name], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print (f"服务 {service_name} 不存在或未运行")
        return False

def toggle_service(service_name, enable):
    action = "enable" if enable else "disable"
    try:
        sudo_cmd = ['sudo', 'systemctl', action, '--now', service_name]
        subprocess.run(sudo_cmd, check=True)
        print(f"服务 {service_name} {action}成功")
    except subprocess.CalledProcessError as e:
        print(f"服务 {service_name} {action}失败:", str(e))

def check_decky_plugin_exists(plugin_name):
    return os.path.isfile(os.path.expanduser("~/homebrew/plugins/{}/plugin.json".format(plugin_name)))


def chk_hibernate():
    file_path = "/etc/systemd/sleep.conf.d/sleep.conf"
    expected_lines = ["#SuspendState=disk", "SuspendState=disk"]

    try:
        with open(file_path, "r") as file:
            content = file.read()
            for line in expected_lines:
                if line in content:
                    return True
    except FileNotFoundError:
        return False

    return False

def chk_grub_quiet_boot():
    file_path = "/etc/default/grub_quiet"
    if not os.path.isfile(file_path):
        return False
    try:
        with open(file_path, "r") as file:
            content = file.readline().strip()
            if "quiet" == content:
                return True
    except FileNotFoundError:
        return False
    
def chk_override_bitrate():
    file_path = "/usr/share/wireplumber/main.lua.d/50-alsa-config.lua"
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return not "--[\"audio.format\"]" in content
    except FileNotFoundError:
        return False
    

def clear_cache():
    command = "sudo rm -rf ~/.cache/sk-holoiso-config/* && sudo rm -rf ~/.local/share/pnpm/store/*"
    return run_command(command, "清除缓存")

def etc_repair():
    command = f"sudo {SK_TOOL_PATH}/etc_repair.sh"
    return run_command(command, "修复 /etc")

def etc_repair_full():
    command = f"sudo {SK_TOOL_PATH}/etc_repair.sh full"
    return run_command(command, "修复 /etc (完全)")

def is_sk_holo2():
    file_path = "/etc/sk-holo/version"
    if not os.path.isfile(file_path):
        return False
    try:
        with open(file_path, "r") as file:
            content = file.readline().strip()
            if "2" == content:
                return True
    except FileNotFoundError:
        return False
    
def chk_firmware_override():
    file_path = "/etc/device-quirks/device-quirks.conf"
    if not os.path.isfile(file_path):
        return False
    try:
        with open(file_path, "r") as file:
            content = file.readlines()
            for line in content:
                if "USE_FIRMWARE_OVERRIDES=1" in line:
                    return True
    except FileNotFoundError:
        return False
    
def get_config_value(filename, section, key):
    config = configparser.ConfigParser()
    config.read(filename)

    if config.has_section(section) and config.has_option(section, key):
        value = config.get(section, key)
        return value
    else:
        return None
    
def get_github_clone_cdn():
    config_file = "/etc/sk-chos-tool/github_cdn.conf"
    cdn = get_config_value(config_file, "clone", "server")
    print("github clone cdn:", cdn)
    if not cdn is None:
        clear_cache()
    return cdn

def check_emudeck_exists():
    appimage_path = "~/Applications/EmuDeck.AppImage"
    # check if appimage exists
    return os.path.isfile(os.path.expanduser(appimage_path))
    