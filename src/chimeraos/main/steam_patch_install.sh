#!/bin/bash
github_url=${1:-"https://github.com"}
echo $github_url
yay -Syy ryzenadj-git jq --needed --noconfirm && \
curl -L "$github_url/honjow/steam-patch/releases/latest/download/install.sh" | sh
