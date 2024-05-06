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

# Disable swipe gestures for QAM and HOME / 禁用游戏模式的侧边滑动手势
disable-swipe-gestures:
    #!/usr/bin/bash
    echo "disabling swipe gestures for QAM and HOME"
    mkdir -p $HOME/.config/environment.d
    conf_file="$HOME/.config/environment.d/chos-disable-gamescope-gestures.conf"
    echo "export GAMESCOPE_DISABLE_TOUCH_GESTURES=1" > "$HOME/.config/environment.d/chos-disable-gamescope-gestures.conf"
    echo "Done. Please restart Steam Game Mode to see changes"

# Enable swipe gestures for QAM and HOME / 启用游戏模式的侧边滑动手势
enable-swipe-gestures:
    #!/usr/bin/bash
    echo "enabling swipe gestures for QAM and HOME"
    conf_file="$HOME/.config/environment.d/chos-disable-gamescope-gestures.conf"
    if [ -f "$conf_file" ]; then
        if grep -q "GAMESCOPE_DISABLE_TOUCH_GESTURES=1" "$conf_file"; then
            sed -i 's/GAMESCOPE_DISABLE_TOUCH_GESTURES=1/GAMESCOPE_DISABLE_TOUCH_GESTURES=0/' "$conf_file"
            echo "Swipe gestures enabled"
        else
            echo "Swipe gestures already enabled"
        fi
    fi
    echo "Done. Please restart Steam Game Mode to see changes"

# etc 修复
etc-repair:
    #!/bin/bash
    if [ -f /usr/share/sk-chos-tool/scripts/etc_repair.sh ]; then
        sudo /usr/share/sk-chos-tool/scripts/etc_repair.sh
    else
        echo "etc-repair not found"
    fi

# etc 修复(完全)
etc-repair-full:
    #!/bin/bash
    if [ -f /usr/share/sk-chos-tool/scripts/etc_repair_full.sh ]; then
        sudo /usr/share/sk-chos-tool/scripts/etc_repair.sh full
    else
        echo "etc-repair-full not found"
    fi

# expand partition / 扩展分区
expand-partition:
    #!/bin/bash
    if [ -f /usr/bin/expand_home_partition ]; then
        sudo /usr/bin/expand_home_partition
    else
        echo "sk-partition-expand not found"
    fi

# expand partition force / 扩展分区（强制）
expand-partition-force:
    #!/bin/bash
    if [ -f /usr/bin/expand_home_partition ]; then
        sudo /usr/bin/expand_home_partition -f
    else
        echo "sk-partition-expand not found"
    fi

# rerun first init / 重新运行首次初始化
rerun-first-init:
    #!/bin/bash
    /usr/bin/sk-first-run