#!/usr/bin/python
# coding=utf-8

import configparser
import os
import subprocess
import glob

from config import logging, SK_TOOL_PATH, USER

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

def get_package_version(package_name):
    try:
        # 运行pacman命令并捕获输出
        result = subprocess.run(['pacman', '-Q', package_name], capture_output=True, text=True, check=True)

        # 获取输出中的版本号部分
        version = result.stdout.strip().split(' ')[1]

        return version
    except subprocess.CalledProcessError:
        return f"Error: Package '{package_name}' not found"

# 检查服务是否已启用
def check_service_autostart(service_name):
    try:
        output = subprocess.check_output(['sudo', 'systemctl', 'is-enabled', service_name]).decode().strip()
        return output == 'enabled'
    except subprocess.CalledProcessError:
        # 如果命令执行出错，则服务可能不存在或无法访问
        return False
    
def check_service_active(service_name):
    try:
        output = subprocess.check_output(['sudo', 'systemctl', 'is-active', service_name]).decode().strip()
        return output == 'active'
    except Exception as e:
        logging.info(f"服务 {service_name} 不存在或无法访问: {e}")
        return False
    
def check_service_exists(service_name):
    try:
        output = subprocess.run(['sudo', 'systemctl', 'status', service_name], capture_output=True, text=True, check=False)
        stderr = output.stderr.strip()
        stdout = output.stdout.strip()

        logging.info(f"check {service_name}\nstderr = {stderr}\nstdout = {stdout}")

        return not "Could not find unit" in stderr and not "Loaded: not-found" in stdout
    except subprocess.CalledProcessError as e:
        logging.info(f"服务 {service_name} 不存在或无法访问: {e}")
        return False

def toggle_service(service_name, enable):
    action = "enable" if enable else "disable"
    try:
        sudo_cmd = ['sudo', 'systemctl', action, '--now', service_name]
        subprocess.run(sudo_cmd, check=True)
        logging.info(f"服务 {service_name} {action}成功")
    except subprocess.CalledProcessError as e:
        logging.error(f"服务 {service_name} {action}失败: {e}")
    except Exception as e:
        logging.error(f"服务 {service_name} {action}失败: {e}")

def check_decky_plugin_exists(plugin_name):
    exists = os.path.isfile(os.path.expanduser(f"~/homebrew/plugins/{plugin_name}/plugin.json"))
    logging.debug(f"检查插件 {plugin_name} 是否存在: {exists}")
    return exists


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

def reset_gnome():
    command = "sudo dconf update && dconf reset -f /"
    success, ret_msg = run_command(command, "重置 GNOME 桌面")
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
    logging.info(f"github clone cdn: {cdn}")
    if not cdn is None:
        clear_cache()
    return cdn

def check_emudeck_exists():
    appimage_path = "~/Applications/EmuDeck.AppImage"
    # check if appimage exists
    return os.path.isfile(os.path.expanduser(appimage_path))
    
def user_noto_fonts_cjk_exists():
    return os.path.isdir(os.path.expanduser("~/.fonts/noto-cjk"))

def check_nix_exists():
    nix_file = "/nix/store/*-nix-*/bin/nix"
    matching_files = glob.glob(nix_file)
    return len(matching_files) > 0

def update_ini_file(file_path, section, key, new_value):
    config = configparser.ConfigParser()

    # 读取配置文件，如果文件不存在，会创建一个新的空文件
    config.read(file_path)

    # 检查类别是否存在，如果不存在则创建
    if not config.has_section(section):
        config.add_section(section)

    # 添加或更新键值对
    config.set(section, key, new_value)

    # 保存配置文件
    with open(file_path, 'w') as configfile:
        config.write(configfile)

def get_config_value(file_path, section, key):
    config = configparser.ConfigParser()
    config.read(file_path)

    if config.has_section(section) and config.has_option(section, key):
        value = config.get(section, key)
        return value
    else:
        return None

def get_autoupdate_config(key):
    conf_dir = f"/home/{USER}/.config/sk-chos-tool"
    os.makedirs(conf_dir, exist_ok=True)
    config_file = f"{conf_dir}/autoupdate.conf"
    section = "autoupdate"
    value = get_config_value(config_file, section, key)
    if value is None:
        value = "true"
        set_autoupdate_config(key, value)
    return value

def set_autoupdate_config(key, value):
    conf_dir = f"/home/{USER}/.config/sk-chos-tool"
    os.makedirs(conf_dir, exist_ok=True)
    config_file = f"{conf_dir}/autoupdate.conf"
    section = "autoupdate"
    update_ini_file(config_file, section, key, value)


def set_autoupdate(pkg_name, enable):
    key = f"autoupdate.{pkg_name}"
    set_autoupdate_config(key, str(enable).lower())

def get_autoupdate(pkg_name):
    key = f"autoupdate.{pkg_name}"
    value = get_autoupdate_config(key)
    return value == "true"
