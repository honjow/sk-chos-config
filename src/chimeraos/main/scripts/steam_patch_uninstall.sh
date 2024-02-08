#!/bin/bash

# curl -L https://github.com/honjow/steam-patch/releases/latest/download/uninstall.sh | sh

sudo systemctl --user stop steam-patch 2> /dev/null
sudo systemctl --user disable steam-patch 2> /dev/null

sudo systemctl stop steam-patch 2> /dev/null
sudo systemctl disable steam-patch 2> /dev/null

yay -Rns sk-steam-patch-git --noconfirm