# vim: set ft=make :

# 设置 flathub 镜像源 (上海交通大学)
flatpak-sjtu:
    flatpak --user remote-modify flathub --url=https://mirror.sjtu.edu.cn/flathub
    sudo flatpak remote-modify flathub --url=https://mirror.sjtu.edu.cn/flathub

# 恢复 flathub 官方源
flatpak-reset:
    flatpak remote-modify flathub --url=https://flathub.org/repo/
    sudo flatpak remote-modify flathub --url=https://flathub.org/repo/