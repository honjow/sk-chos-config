#!/usr/bin/python
# coding=utf-8
import os
import urllib.request

# import utils
from utils import run_command, toggle_service


def handycon_switch_callback(active):
    toggle_service("handycon.service", active)

def oxp2lsusb_switch_callback(active):
    toggle_service("oxp2-lsusb.service", active)

def oxp2_volume_button_fix_switch_callback(active):
    toggle_service("oxp2-volume-button-fix.service", active)

# ayaneo 切换lc键睡眠
def aya_lc_suspend_switch_callback(active):
    toggle_flag_file = '/usr/share/handygccs/aya-lc-suspend'
    toggle_flag_file_exists = os.path.isfile(toggle_flag_file)
    if active and not toggle_flag_file_exists:
        # 创建文件 并 重启服务
        run_command('sudo touch {} && sudo systemctl restart handycon.service'.format(toggle_flag_file))
    elif not active and toggle_flag_file_exists:
        # 删除文件 并 重启服务
        run_command('sudo rm {} && sudo systemctl restart handycon.service'.format(toggle_flag_file))


def handycon_install():
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

def handycon_uninstall():
    print("执行 HandyGCCS 卸载操作")
    command = ("sudo systemctl stop handycon && sudo systemctl disable handycon;"
                "sudo rm -v /usr/lib/modules-load.d/handycon.conf;"
                "sudo rm -v /usr/lib/systemd/system/handycon.service;"
                "sudo rm -v /usr/lib/udev/rules.d/60-handycon.rules;"
                "sudo rm -v /usr/share/handygccs/scripts/constants.py;"
                "sudo rm -v /usr/share/handygccs/scripts/handycon.py;"
                "sudo rm -v /usr/share/libretro/autoconfig/udev/HandyGCCS-Controller.cfg;"
                "sudo udevadm control -R"
                )
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

def simple_decky_install():
    command = "curl -Lk https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh | sed 's#prerelease == \"false\"#prerelease == \"true\"#' | sudo sh"
    return run_command(command, "Decky")

def tomoon_install():
    command = "curl -L http://i.ohmydeck.net | sed 's#curl#curl -k#g' | sh"
    # command = "ls /abcd"
    return run_command(command, "ToMoon")

def this_app_install():
    command = "yay -Sy sk-holoiso-config --noconfirm --overwrite \"*\""
    success, ret_msg = run_command(command, "Sk Holoiso Config")
    if success:
        ret_msg = "更新完成, 请重新启动应用"
    return success, ret_msg

def decky_plugin_update(git_url):
    depends_command = "yay -Sy npm --noconfirm --needed"
    success, ret_msg = run_command(depends_command, "npm")
    if not success:
        return success, ret_msg

    name = git_url.split("/")[-1].split(".")[0]
    print("执行Decky插件更新操作 {} {}".format(name, git_url))
    git_directory = os.path.expanduser("~/.cache/sk-holoiso-config/git")
    repo_directory = os.path.expanduser("{}/{}".format(git_directory, name))
    if os.path.exists(repo_directory):
        upt_command = "cd {} && git pull".format(repo_directory)
    else:
        upt_command = ("mkdir -p {} && cd {} && git clone {}").format(git_directory, git_directory, git_url)
    print("执行更新命令: {}".format(upt_command))

    success, ret_msg = run_command(upt_command, name)
    if not success:
        return success, ret_msg

    build_command = "cd {} && sudo npm i -g pnpm && pnpm i && pnpm update decky-frontend-lib --latest && pnpm run build".format(repo_directory)
    success, ret_msg = run_command(build_command, name)
    if not success:
        return success, ret_msg
    
    # parse plugin.json 
    plugin_json_path = "{}/plugin.json".format(repo_directory)
    if not os.path.exists(plugin_json_path):
        return False, "plugin.json 不存在"
    import json
    with open(plugin_json_path, "r") as f:
        plugin_json = json.load(f)
    plugin_name = plugin_json["name"]
    plugin_parent_directory = os.path.expanduser("~/homebrew/plugins")
    plugin_directory = os.path.expanduser("{}/{}".format(plugin_parent_directory, plugin_name))

    deploy_command = (f"chmod -v 755 {plugin_parent_directory} "
                        f" && mkdir -p {plugin_directory} "
                        f" && chmod -v 755 {plugin_directory} "
                        f" && rsync -azp --progress --delete {repo_directory}/ {plugin_directory} "
                        " --chmod=Du=rwx,Dg=rx,Do=rx,Fu=rwx,Fg=rx,Fo=rx "
                        " --exclude='.git/' --exclude='.github/' --exclude='.vscode/' --exclude='node_modules/' "
                        " --exclude='.pnpm-store/' --exclude='src/' --exclude='*.log' --exclude='.gitignore'  "
                        " --exclude='.idea' --exclude='.env' --exclude='Makefile' --exclude='pnpm-lock.yaml' "
                        " && sudo systemctl restart plugin_loader.service "
                        )
    
    # print ("执行部署命令: {}".format(deploy_command))
    # os.system(deploy_command)
    return run_command(deploy_command, name)

def remove_decky_plugin(plugin_name):
    command = "sudo rm -rf ~/homebrew/plugins/{} && sudo systemctl restart plugin_loader.service ".format(plugin_name)
    return run_command(command, plugin_name)

def power_control_install():
    git_url = "https://github.com/mengmeet/PowerControl.git"
    return decky_plugin_update(git_url)

def ayaled_install():
    git_url = "https://github.com/MiZai2/ayaled.git"
    return decky_plugin_update(git_url)


def mesa_arch_install():
    command = "sudo /usr/share/sk-holoiso-config/install_mesa_arch.sh"
    return run_command(command, "Mesa Arch")

def mesa_valve_install():
    # check gpu vendor
    chk_780m_command = "lspci | grep VGA |grep -i amd | grep -i 780m"
    chk_780m_result = os.popen(chk_780m_command).read()
    if chk_780m_result:
        return False, "暂不支持 Radeon 780M"

    command = "sudo /usr/share/sk-holoiso-config/install_mesa_valve.sh"
    return run_command(command, "Mesa Valve")
