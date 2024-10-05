# vim: set ft=make :

# some from https://github.com/ublue-os/config/blob/main/build/ublue-os-just

# make swapfile / 创建交换文件 参数可空 单位 GB
mkswapfile SIZE="":
    #!/bin/bash
    sudo /usr/bin/sk-mkswapfile {{SIZE}}

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
    echo "禁用游戏模式的侧边滑动手势"
    mkdir -p $HOME/.config/environment.d
    conf_file="$HOME/.config/environment.d/chos-disable-gamescope-gestures.conf"
    if (gamescope --help 2>&1 | grep -e "--touch-gestures" > /dev/null); then
        rm -f "$conf_file"
        export GAMESCOPE_TOUCH_GESTURES=""
    else
        echo "GAMESCOPE_DISABLE_TOUCH_GESTURES=1" > "$conf_file"
    fi
    echo "操作完成，请重启 Steam 游戏模式以应用更改"

# Enable swipe gestures for QAM and HOME / 启用游戏模式的侧边滑动手势
enable-swipe-gestures:
    #!/usr/bin/bash
    echo "启用游戏模式的侧边滑动手势"
    conf_file="$HOME/.config/environment.d/chos-disable-gamescope-gestures.conf"
    if (gamescope --help 2>&1 | grep -e "--touch-gestures" > /dev/null); then
        echo "GAMESCOPE_TOUCH_GESTURES=1" > "$conf_file"
    else
        if [ -f "$conf_file" ]; then
            if grep -q "GAMESCOPE_DISABLE_TOUCH_GESTURES=1" "$conf_file"; then
                echo "" > "$conf_file"
                echo "Swipe gestures enabled"
            else
                echo "Swipe gestures already enabled"
            fi
        fi
    fi
    echo "操作完成，请重启 Steam 游戏模式以应用更改"

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

# run first setup / 运行首次设置
run-first-setup:
    #!/bin/bash
    /usr/bin/sk-first-setup

# set TDP / 设置 TDP
alias tdp := set-tdp

# set TDP / 设置 TDP
set-tdp tdp_num:
    #!/bin/bash
    tdp_watt=$(({{tdp_num}} * 1000))
    if [ -x $(command -v ryzenadj) ]; then
        sudo ryzenadj --stapm-limit $tdp_watt --fast-limit $tdp_watt --slow-limit $tdp_watt
    else
        echo "ryzenadj not found"
    fi

# toggle use mirrors to update / 切换使用镜像地址更新
toggle-mirrors:
    #!/bin/bash
    conf_file="/etc/frzr-sk.conf"
    if [ -f "$conf_file" ]; then
        # 如果包含 fallback_url = xxxx, 获取 xxxx
        fallback_url=$(grep -oP 'fallback_url\s*=\s*\K.*' "$conf_file")
        if [ "$fallback_url" = "false" ]; then
            sudo sed -i 's/fallback_url\s*=\s*false/fallback_url = true/' "$conf_file"
        else
            sudo sed -i 's/fallback_url\s*=\s*true/fallback_url = false/' "$conf_file"
        fi
    else
        echo "fallback_url = false" | sudo tee "$conf_file"
    fi
