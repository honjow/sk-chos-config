#!/usr/bin/python
# coding=utf-8
import os
import urllib.request

# import utils
from utils import run_command


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