#!/bin/bash
github_prefix=$1
echo $github_prefix
yay -Sy ryzenadj-git jq --needed --noconfirm && \
curl -o /tmp/sp_install_cn.sh -L "${github_url}https://github.com/honjow/steam-patch/releases/latest/download/install_cn.sh" && \
chmod +x /tmp/sp_install_cn.sh && /tmp/sp_install_cn.sh $github_prefix
