#!/bin/bash
# github_prefix=$1
# echo $github_prefix
# # yay -Sy ryzenadj-git jq --needed --noconfirm && \
# curl -o /tmp/sp_install_cn.sh -L "${github_prefix}https://github.com/honjow/steam-patch/releases/latest/download/install_cn.sh" && \
# chmod +x /tmp/sp_install_cn.sh && /tmp/sp_install_cn.sh $github_prefix

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