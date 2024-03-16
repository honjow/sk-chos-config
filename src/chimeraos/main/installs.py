#!/usr/bin/python
# coding=utf-8
import os
import urllib.request

# import utils
from utils import get_github_clone_cdn, get_github_raw_cdn, get_github_release_cdn, run_command, toggle_service

from config import SK_TOOL_SCRIPTS_PATH, logging, USER

def handycon_switch_callback(active):
    toggle_service(f"hhd@{os.getenv('USER')}.service", not active)
    toggle_service("handycon.service", active)

def hhd_switch_callback(active):
    toggle_service("handycon.service", not active)
    toggle_service(f"hhd@{os.getenv('USER')}.service", active)

def oxp2lsusb_switch_callback(active):
    toggle_service("oxp2-lsusb.service", active)

def oxp2_volume_button_fix_switch_callback(active):
    toggle_service("oxp2-volume-button-fix.service", active)

def sk_auto_keep_boot_entry_switch_callback(active):
    toggle_service("sk-auto-keep-boot-entry.service", active)

def auto_update_switch_callback(active):
    toggle_service("sk-chos-tool-autoupdate.timer", active)

def hibernate_switch_callback(active):
    old_file = "/etc/systemd/sleep.conf.d/sleep.conf"
    # 判断文件是否存在
    old_file_exists = os.path.isfile(old_file)
    if old_file_exists:
        run_command("sudo rm -f /etc/systemd/sleep.conf.d/sleep.conf")
        run_command("sudo systemctl kill -s HUP systemd-logind")

    if active:
        run_command("sudo cp /lib/systemd/system/systemd-hibernate.service /etc/systemd/system/systemd-suspend.service")
    else:
        run_command("sudo rm -f /etc/systemd/system/systemd-suspend.service")
    # 生效
    run_command("sudo systemctl daemon-reload")

def grub_quiet_boot_switch_callback(active):
    if active:
        run_command(f"sudo bash {SK_TOOL_SCRIPTS_PATH}/grub_quiet_boot_enable.sh")
    else:
        run_command(f"sudo bash {SK_TOOL_SCRIPTS_PATH}/grub_quiet_boot_disable.sh")
    # 生效
    run_command("sudo update-grub")

def override_bitrate_switch_callback(active):
    if active:
        run_command(f"sudo bash {SK_TOOL_SCRIPTS_PATH}/override_bitrate_enable.sh")
    else:
        run_command(f"sudo bash {SK_TOOL_SCRIPTS_PATH}/override_bitrate_disable.sh")


# ayaneo 切换lc键睡眠
def aya_lc_suspend_switch_callback(active):
    toggle_flag_file = '/etc/handygccs/special_suspend'
    toggle_flag_file_exists = os.path.isfile(toggle_flag_file)
    if active and not toggle_flag_file_exists:
        # 创建文件
        run_command('sudo touch {}'.format(toggle_flag_file))
    elif not active and toggle_flag_file_exists:
        # 删除文件
        run_command('sudo rm {}'.format(toggle_flag_file))

def handycon_install():
    logging.info("执行 HandyGCCS 更新操作")
    command = ("__handygccs-update && sudo systemctl restart handycon.service")
    return run_command(command, "HandyGCCS 更新")

def handycon_install_old():
    logging.info("执行 HandyGCCS 更新操作")
    github_cdn_url = get_github_clone_cdn()
    git_url = "https://github.com/honjow/HandyGCCS.git"
    if github_cdn_url:
        git_url = git_url.replace("https://github.com", github_cdn_url)

    # 解决 pip install 时 error: externally-managed-environment 问题
    os.system("sudo rm -f /usr/lib/python3.11/EXTERNALLY-MANAGED")

    os.system("sudo pacman -Sy python-installer python-build python-wheel python-setuptools --needed --noconfirm")

    # 判断 ~/.cache/sk-holoiso-config/git/HandyGCCS 是否存在
    git_directory = os.path.expanduser("~/.cache/sk-holoiso-config/git/HandyGCCS")
    if os.path.exists(git_directory):
        logging.info("更新git目录并执行更新")
        command = ("cd {} && git checkout main"
                   " && git checkout . && git pull"
                   " && sudo ./build.sh && sleep 3"
                   " && sudo systemctl daemon-reload"
                   " && sudo systemctl restart handycon.service"
                   ).format(git_directory)
    else:
        logging.info("新建git目录并执行更新")
        command = ("mkdir -p ~/.cache/sk-holoiso-config/git "
                   " && cd ~/.cache/sk-holoiso-config/git "
                   " && git clone {} -b main HandyGCCS "
                   " && cd HandyGCCS "
                   " && sudo ./build.sh"
                   " && sleep 3"
                   " && sudo systemctl daemon-reload"
                   " && sudo systemctl restart handycon.service"
                   ).format(git_url, git_directory)

    return run_command(command, "HandyGCCS 更新")

def handycon_uninstall_old():
    logging.info("执行 HandyGCCS 卸载操作")
    command = ("sudo systemctl stop handycon && sudo systemctl disable handycon;"
                "sudo rm -rf /usr/lib/python3*/site-packages/handycon*;"
                "sudo rm /usr/bin/handycon;"
                "sudo rm -rf /usr/share/handygccs;"
                "sudo rm -rf /etc/handygccs;"
                "sudo rm /usr/lib/systemd/system/handycon.service;"
                "sudo rm /usr/lib/udev/hwdb.d/59-handygccs-ayaneo.hwdb;"
                "sudo rm /usr/lib/udev/rules.d/60-handycon.rules;"
                "sudo systemd-hwdb update;"
                "sudo udevadm control -R;"
                )
    return run_command(command, "HandyGCCS")

def handycon_uninstall():
    logging.info("执行 HandyGCCS 卸载操作")
    command = ("sudo systemctl stop handycon && sudo systemctl disable handycon && sudo pacman -R handygccs-git --noconfirm")
    return run_command(command, "HandyGCCS 卸载")

def hhd_install():
    logging.info("执行 HHD 更新操作")
    command = (f"__hhd-update && sudo systemctl restart hhd@{USER}.service")
    return run_command(command, "HHD 更新")

def hhd_uninstall():
    logging.info("执行 HHD 卸载操作")
    hhd_path="/usr/bin/hhd"
    hhd_owner_comand = "LANG=en_US pacman -Qo {} 2>/dev/null | awk '{print $5}'".format(hhd_path)
    hhd_owner = os.popen(hhd_owner_comand).read().strip()
    command = (f"sudo systemctl stop hhd@{USER} && sudo systemctl disable hhd@{USER} && sudo pacman -R {hhd_owner} --noconfirm")
    return run_command(command, "HHD 卸载")

def decky_update_callback():
    success = True
    ret_msg = None
    github_cdn_url = get_github_clone_cdn()
    logging.info("执行Decky更新操作")
    
    # 判断 ~/.cache/sk-holoiso-config/user_install_script.sh 是否存在
    script_path = os.path.expanduser("~/.cache/sk-holoiso-config/user_install_script.sh")
    if os.path.exists(script_path):
        # 删除已存在的脚本文件
        os.remove(script_path)
    # 下载最新的脚本文件
    script_url = "https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/user_install_script.sh"
    if github_cdn_url:
        script_url = script_url.replace("https://github.com", github_cdn_url)
    try:
        urllib.request.urlretrieve(script_url, script_path)
        logging.info("脚本文件下载完成")
    except Exception as e:
        logging.error(f"下载脚本文件时出现错误: {e}")
        success = False
        ret_msg = str(e)
        return success, ret_msg
    # 给脚本文件添加执行权限
    os.chmod(script_path, 0o755)
    # 在bash中执行脚本文件
    os.system("sudo sh {}".format(script_path))
    logging.info("Decky更新完成")
    return success, ret_msg

def simple_decky_install():
    # command = "curl -Lk https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh | sed 's#prerelease == \"false\"#prerelease == \"true\"#' | sh"
    git_url="https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh"
    # github_cdn_url = get_github_clone_cdn()
    # if github_cdn_url:
    #     git_url = git_url.replace("https://github.com", github_cdn_url)
    command = "curl -sLk {} | sed 's#prerelease == \"false\"#prerelease == \"true\"#' | sh".format(git_url)
    return run_command(command, "Decky")

def simple_cn_decky_install():
    command = "curl -L http://dl.ohmydeck.net | sh"
    return run_command(command, "Decky (CN)")

def tomoon_install():
    command = "curl -L http://i.ohmydeck.net | sed 's#/home/deck#/home/gamer#' | sed 's#curl#curl -k#g' | sh"
    return run_command(command, "ToMoon")

def this_app_install():
    command = "yay -Sy sk-chos-tool --noconfirm --overwrite \"*\""
    success, ret_msg = run_command(command, "Sk ChimeraOS Tool")
    if success:
        ret_msg = "更新完成, 请重新启动应用"
    return success, ret_msg

def this_app_cn_install():
    command = "curl -L https://gitee.com/honjow/sk-chos-scripts/raw/master/install/install-sk-chos-tool.sh | sh"
    success, ret_msg = run_command(command, "Sk ChimeraOS Tool (CN)")
    if success:
        ret_msg = "更新完成, 请重新启动应用"
    return success, ret_msg

def decky_plugin_update(git_url, p_name=None):
    depends_command = "yay -Sy npm --noconfirm --needed && sudo npm i -g pnpm"
    success, ret_msg = run_command(depends_command, "npm pnpm")
    if not success:
        return success, ret_msg

    name = git_url.split("/")[-1].split(".")[0]
    logging.info(f"执行Decky插件更新操作 {name} {git_url}")
    git_directory = os.path.expanduser("~/.cache/sk-holoiso-config/git")
    repo_directory = os.path.expanduser("{}/{}".format(git_directory, name))

    if os.path.exists(repo_directory):
        delete_command = "rm -rf {}".format(repo_directory)
        logging.info("执行删除命令: {}".format(delete_command))
        success, ret_msg = run_command(delete_command, name)

    if os.path.exists(repo_directory):
        upt_command = "cd {} && git checkout . && git pull".format(repo_directory)
    else:
        upt_command = ("mkdir -p {} && cd {} && git clone {}").format(git_directory, git_directory, git_url)
    logging.info(f"执行更新命令: {upt_command}")

    success, ret_msg = run_command(upt_command, name)
    if not success:
        return success, ret_msg

    build_command = "cd {} && rm -rf node_modules pnpm-lock.yaml && pnpm i && pnpm update decky-frontend-lib --latest && pnpm run build".format(repo_directory)
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
    plugin_name = p_name if p_name else plugin_json["name"]
    plugin_parent_directory = os.path.expanduser("~/homebrew/plugins")
    plugin_directory = os.path.expanduser("{}/{}/".format(plugin_parent_directory, plugin_name))
    
    # if plugin_directory contains space
    if " " in plugin_directory:
        plugin_directory = plugin_directory.replace(" ", "-")

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
    
    return run_command(deploy_command, name)

def remove_decky_plugin(plugin_name):
    command = "sudo rm -rf ~/homebrew/plugins/{} && sudo systemctl restart plugin_loader.service ".format(plugin_name)
    return run_command(command, plugin_name)

def power_control_install():
    git_url = "https://github.com/mengmeet/PowerControl.git"
    github_cdn_url = get_github_clone_cdn()
    if github_cdn_url:
        git_url = git_url.replace("https://github.com", github_cdn_url)
    return decky_plugin_update(git_url)

def power_control_bin_install():
    release_prefix = get_github_release_cdn()
    command = f"{SK_TOOL_SCRIPTS_PATH}/power_control_install.sh {release_prefix}"
    return run_command(command, "PowerControl bin")

def huesync_bin_install():
    release_prefix = get_github_release_cdn()
    command = f"{SK_TOOL_SCRIPTS_PATH}/huesync_install.sh {release_prefix}"
    return run_command(command, "HueSync bin")

def hhd_decky_bin_install():
    release_prefix = get_github_release_cdn()
    command = f"{SK_TOOL_SCRIPTS_PATH}/hhd_decky_install.sh {release_prefix}"
    return run_command(command, "HHD-Decky bin")

def huesync_install():
    git_url = "https://github.com/honjow/huesync.git"
    github_cdn_url = get_github_clone_cdn()
    if github_cdn_url:
        git_url = git_url.replace("https://github.com", github_cdn_url)
    return decky_plugin_update(git_url)

def LegionGoRemapper_install():
    git_url = "https://github.com/aarron-lee/LegionGoRemapper.git"
    github_cdn_url = get_github_clone_cdn()
    if github_cdn_url:
        git_url = git_url.replace("https://github.com", github_cdn_url)
    return decky_plugin_update(git_url)

def mango_peel_install():
    git_url = "https://github.com/honjow/MangoPeel.git"
    github_cdn_url = get_github_clone_cdn()
    if github_cdn_url:
        git_url = git_url.replace("https://github.com", github_cdn_url)
    return decky_plugin_update(git_url)

def simple_decky_TDP_install():
    git_url = "https://github.com/aarron-lee/SimpleDeckyTDP.git"
    github_cdn_url = get_github_clone_cdn()
    if github_cdn_url:
        git_url = git_url.replace("https://github.com", github_cdn_url)
    return decky_plugin_update(git_url)

def hhd_decky_install():
    git_url = "https://github.com/hhd-dev/hhd-decky.git"
    github_cdn_url = get_github_clone_cdn()
    if github_cdn_url:
        git_url = git_url.replace("https://github.com", github_cdn_url)
    return decky_plugin_update(git_url, p_name="hhd-decky")

def emudeck_decky_controls_install():
    git_url = "https://github.com/EmuDeck/emudeck-decky-controls.git"
    github_cdn_url = get_github_clone_cdn()
    if github_cdn_url:
        git_url = git_url.replace("https://github.com", github_cdn_url)
    return decky_plugin_update(git_url, p_name="emudeck-decky-controls")

def mesa_arch_install():
    command = f"sudo {SK_TOOL_SCRIPTS_PATH}/install_mesa_arch.sh"
    return run_command(command, "Mesa Arch")

def mesa_valve_install():
    command = f"sudo {SK_TOOL_SCRIPTS_PATH}/install_mesa_valve.sh"
    return run_command(command, "Mesa Valve")

def steam_patch_install():
    github_cdn_url = get_github_clone_cdn()
    github_prefix = github_cdn_url.replace("https://github.com", "")
    command = f"{SK_TOOL_SCRIPTS_PATH}/steam_patch_install.sh {github_prefix}"
    return run_command(command, "Steam Patch")

def steam_patch_uninstall():
    command = f"{SK_TOOL_SCRIPTS_PATH}/steam_patch_uninstall.sh"
    return run_command(command, "Steam Patch")

def firmware_override_switch_callback(enable):
    if enable:
        run_command("sudo sk-firmware-override enable")
    else:
        run_command("sudo sk-firmware-override disable")

def usb_wakeup_switch_callback(enable):
    conf_path = "/etc/device-quirks/device-quirks.conf"
    enable_str = "USB_WAKE_ENABLED=1"
    disable_str = "USB_WAKE_ENABLED=0"
    if enable:
        logging.info("开启USB唤醒")
        run_command(f"sudo sed -i 's/{disable_str}/{enable_str}/g' {conf_path}")
    else:
        logging.info("关闭USB唤醒")
        run_command(f"sudo sed -i 's/{enable_str}/{disable_str}/g' {conf_path}")
    run_command("sudo frzr-tweaks")
    logging.info("USB唤醒设置完成")

def emudeck_install():
    release_prefix = get_github_release_cdn()
    raw_prefix = get_github_raw_cdn()
    command = f"bash {SK_TOOL_SCRIPTS_PATH}/emudeck_install.sh {release_prefix} {raw_prefix}"
    return run_command(command, "EmuDeck")

def noto_fonts_cjk_install():
    command = f"{SK_TOOL_SCRIPTS_PATH}/noto_fonts_cjk_install.sh install"
    return run_command(command, "Noto CJK Fonts")

def noto_fonts_cjk_uninstall():
    command = f"{SK_TOOL_SCRIPTS_PATH}/noto_fonts_cjk_install.sh uninstall"
    return run_command(command, "Noto CJK Fonts")

def spb_lego_exist():
    path = "~/homebrew/themes/SBP-Legion-Go-Theme"
    path = os.path.expanduser(path)
    return os.path.exists(path)

def spb_lego_install():
    command = "curl -L https://raw.githubusercontent.com/honjow/sk-holoiso-config/master/scripts/install-SBP-Legion-Go-Theme.sh | sh"
    return run_command(command, "SBP-Legion-Go-Theme")

def spb_lego_uninstall():
    path = "~/homebrew/themes/SBP-Legion-Go-Theme"
    command = f"rm -rf {path}"
    return run_command(command, "SBP-Legion-Go-Theme")

def ps5_to_h_exist():
    path = "~/homebrew/themes/SBP-PS5-to-Handheld"
    path = os.path.expanduser(path)
    return os.path.exists(path)

def ps5_to_h_install():
    command = "curl -sL https://github.com/honjow/SBP-PS5-to-Handheld/raw/master/install.sh | sh"
    return run_command(command, "SBP-PS5-to-Handheld")

def ps5_to_h_uninstall():
    path = "~/homebrew/themes/SBP-PS5-to-Handheld"
    command = f"rm -rf {path}"
    return run_command(command, "SBP-PS5-to-Handheld")

def nix_install():
    command = f"/usr/bin/sk-nix-install install"
    return run_command(command, "Nix")

def nix_uninstall():
    command = f"/usr/bin/sk-nix-install uninstall"
    return run_command(command, "Nix")