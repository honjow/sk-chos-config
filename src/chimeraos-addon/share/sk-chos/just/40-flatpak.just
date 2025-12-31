# vim: set ft=make :

lang := `echo $LANG | cut -d. -f1`

# 设置 flathub 镜像源 (上海交通大学)
[group("system")]
flatpak-sjtu:
    #!/bin/bash
    flatpak --user remote-add --if-not-exists flathub https://mirror.sjtu.edu.cn/flathub
    flatpak --user remote-modify flathub --url=https://mirror.sjtu.edu.cn/flathub
    sudo flatpak remote-add --if-not-exists flathub https://mirror.sjtu.edu.cn/flathub
    sudo flatpak remote-modify flathub --url=https://mirror.sjtu.edu.cn/flathub

# 恢复 flathub 官方源
[group("system")]
flatpak-reset:
    #!/bin/bash
    flatpak --user remote-add --if-not-exists flathub https://flathub.org/repo/
    flatpak --user remote-modify flathub --url=https://flathub.org/repo/
    sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/
    sudo flatpak remote-modify flathub --url=https://flathub.org/repo/

# 显示 flathub 源
[group("system")]
flatpak-remotes:
    flatpak remotes --columns=name,options,url

# 自动设置 flathub 镜像源
[group("system")]
flatpak-auto-repo:
    #!/bin/bash
    if [ {{lang}} == "zh_CN" ]; then
        cjust flatpak-sjtu
    else
        cjust flatpak-reset
    fi