# vim: set ft=make :

# make swapfile / 重新生成 swapfile
mkswapfile:
    #!/bin/bash
    sudo /usr/bin/sk-mkswapfile

# fix boot entry / 修复启动项
boot-entry-fix:
    #!/bin/bash
    sudo /usr/bin/sk-chos-boot-fix

# HHD fast QAM 切换
hhd-fast-qam-toggle:
    #!/bin/bash
    conf_file="$HOME/.config/environment.d/99-hhd-fast-qam.conf"
    if [ ! -f "$conf_file" ]; then
        echo "HHD_QAM_GAMESCOPE=1" > "$conf_file"
        echo "hhd fast qam enabled"
        exit 0
    fi
    if [ ! -d "$HOME/.config/environment.d" ]; then
        mkdir -p "$HOME/.config/environment.d"
    fi
    if grep -q "HHD_QAM_GAMESCOPE=1" "$conf_file"; then
        sed -i 's/HHD_QAM_GAMESCOPE=1/HHD_QAM_GAMESCOPE=0/' "$conf_file"
        echo "hhd fast qam disabled"
    else
        sed -i 's/HHD_QAM_GAMESCOPE=0/HHD_QAM_GAMESCOPE=1/' "$conf_file"
        echo "hhd fast qam enabled"
    fi

# Handheld Daemon enable / 启用 Handheld Daemon
hhd-enable:
    #!/bin/bash
    sudo systemctl enable --now hhd@$(whoami).service

# Handheld Daemon disable / 停用 Handheld Daemon
hhd-disable:
    #!/bin/bash
    sudo systemctl disable --now hhd@$(whoami).service

# InputPlumber enable / 启用 InputPlumber
inputplumber-enable:
    #!/bin/bash
    sudo systemctl enable --now inputplumber.service

# InputPlumber disable / 停用 InputPlumber
inputplumber-disable:
    #!/bin/bash
    sudo systemctl disable --now inputplumber.service

# 静默启动开启 / quiet boot enable
quiet-boot-enable:
    #!/bin/bash
    if [ -f /usr/share/device-quirks/scripts/kernel-options-manager ]; then
        sudo /usr/share/device-quirks/scripts/kernel-options-manager --append quiet
    else
        echo "kernel-options-manager not found"
    fi

# 静默启动关闭 / quiet boot disable
quiet-boot-disable:
    #!/bin/bash
    if [ -f /usr/share/device-quirks/scripts/kernel-options-manager ]; then
        sudo /usr/share/device-quirks/scripts/kernel-options-manager --remove quiet
    else
        echo "kernel-options-manager not found"
    fi