#!/bin/bash
# github_prefix=$1
# echo $github_prefix
# # yay -Sy ryzenadj-git jq --needed --noconfirm && \
# curl -o /tmp/sp_install_cn.sh -L "${github_prefix}https://github.com/honjow/steam-patch/releases/latest/download/install_cn.sh" && \
# chmod +x /tmp/sp_install_cn.sh && /tmp/sp_install_cn.sh $github_prefix

# cant run this script as root
if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as a normal user, not root."
    exit 1
fi

OLD_DIR="$HOME/steam-patch"

# 获取 $USER_DIR/steam-patch 的所属用户 如果是root， 则删除
if [ -d "$OLD_DIR" ]; then
    USER_DIR_OWNER=$(stat -c '%U' $OLD_DIR)
    if [ "$USER_DIR_OWNER" == "root" ]; then
        sudo rm -rf $OLD_DIR
    fi
fi

mkdir -p $HOME/steam-patch

sudo systemctl --user stop steam-patch 2> /dev/null
sudo systemctl --user disable steam-patch 2> /dev/null

sudo systemctl stop steam-patch 2> /dev/null
sudo systemctl disable steam-patch 2> /dev/null

sudo rm -f /etc/systemd/system/steam-patch.service

yay -Sy sk-steam-patch-git --overwrite "*" --needed --noconfirm

sudo systemctl daemon-reload
sudo systemctl enable steam-patch.service
sudo systemctl start steam-patch.service
sudo systemctl enable restart-steam-patch-on-boot.service
sudo systemctl start restart-steam-patch-on-boot.service