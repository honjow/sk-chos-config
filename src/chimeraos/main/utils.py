#!/usr/bin/python
# coding=utf-8

import configparser
import os
import subprocess

from config import logging, SK_TOOL_PATH

def get_product_name():
    # get from /sys/devices/virtual/dmi/id/product_name
    product_name = ""
    try:
        with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
            product_name = f.readline().strip()
    except Exception as e:
        logging.error("读取设备名称失败:", str(e))
    logging.info("设备名称:", product_name)
    return product_name

# 执行命令
def run_command(command, name=""):
    success = True
    ret_msg = ""
    logging.info(f"执行{name}操作")
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in process.stdout:
            logging.info(line.strip())
        stdout, stderr = process.communicate()
        return_code = process.returncode

        if return_code != 0:
            success = False
            ret_msg = stderr.strip()
            logging.error(f"{name}操作失败: {ret_msg}")
        else:
            logging.info(f"{name}操作完成")
    except Exception as e:
        success = False
        ret_msg = str(e)
        logging.error(f"{name}操作失败: {ret_msg}")
    
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
        subprocess.run(['sudo', 'systemctl', 'is-active', service_name], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        logging.error(f"服务 {service_name} 不存在或未运行")
        return False

def toggle_service(service_name, enable):
    action = "enable" if enable else "disable"
    try:
        sudo_cmd = ['sudo', 'systemctl', action, '--now', service_name]
        subprocess.run(sudo_cmd, check=True)
        logging.info(f"服务 {service_name} {action}成功")
    except subprocess.CalledProcessError as e:
        logging.error(f"服务 {service_name} {action}失败:", str(e))

def check_decky_plugin_exists(plugin_name):
    return os.path.isfile(os.path.expanduser("~/homebrew/plugins/{}/plugin.json".format(plugin_name)))


def chk_hibernate():
    file_path = "/etc/systemd/system/systemd-suspend.service"
    check_content = "systemd-sleep hibernate"

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if check_content in line:
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

def boot_repair():
    command = "sudo /usr/bin/sk-chos-boot-fix"
    return run_command(command, "修复启动项")

def etc_repair():
    command = f"sudo {SK_TOOL_PATH}/etc_repair.sh"
    success, ret_msg = run_command(command, "修复 /etc")
    if success:
        ret_msg = "重置完成, 重启生效"
    return success, ret_msg

def make_swapfile():
    command = f"sudo {SK_TOOL_PATH}/make_swapfile.sh"
    success, ret_msg = run_command(command, "重新创建swapfile")
    if success:
        ret_msg = "重新创建swapfile完成, 重启生效"
    return success, ret_msg

def etc_repair_full():
    command = f"sudo {SK_TOOL_PATH}/etc_repair.sh full"
    success, ret_msg = run_command(command, "修复 /etc (完全)")
    if success:
        ret_msg = "重置完成, 重启生效"
    return success, ret_msg

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
    logging.info("github clone cdn:", cdn)
    if not cdn is None:
        clear_cache()
    return cdn

def check_emudeck_exists():
    appimage_path = "~/Applications/EmuDeck.AppImage"
    # check if appimage exists
    return os.path.isfile(os.path.expanduser(appimage_path))
    
def user_noto_fonts_cjk_exists():
    return os.path.isdir(os.path.expanduser("~/.fonts/noto-cjk"))