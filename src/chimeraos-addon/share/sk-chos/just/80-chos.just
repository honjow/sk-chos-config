# vim: set ft=make :

# make swapfile / 重新生成 swapfile
mkswapfile:
    sudo /usr/bin/sk-mkswapfile

# fix boot entry / 修复启动项
boot-entry-fix:
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
    if grep -q "HHD_QAM_GAMESCOPE=1" "$conf_file"; then
        sed -i 's/HHD_QAM_GAMESCOPE=1/HHD_QAM_GAMESCOPE=0/' "$conf_file"
        echo "hhd fast qam disabled"
    else
        sed -i 's/HHD_QAM_GAMESCOPE=0/HHD_QAM_GAMESCOPE=1/' "$conf_file"
        echo "hhd fast qam enabled"
    fi
