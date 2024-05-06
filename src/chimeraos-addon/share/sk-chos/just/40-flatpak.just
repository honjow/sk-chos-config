# vim: set ft=make :

lang := `echo $LANG | cut -d. -f1`

# 设置 flathub 镜像源 (上海交通大学)
flatpak-sjtu:
    flatpak --user remote-modify flathub --url=https://mirror.sjtu.edu.cn/flathub
    sudo flatpak remote-modify flathub --url=https://mirror.sjtu.edu.cn/flathub

# 恢复 flathub 官方源
flatpak-reset:
    flatpak remote-modify flathub --url=https://flathub.org/repo/
    sudo flatpak remote-modify flathub --url=https://flathub.org/repo/

# 显示 flathub 源
flatpak-remotes:
    flatpak remotes --columns=name,url

# 自动设置 flathub 镜像源
flatpak-auto-repo:
    #!/bin/bash
    if [ {{lang}} == "zh_CN" ]; then
        cjust flatpak-sjtu
    else
        cjust flatpak-reset
    fi