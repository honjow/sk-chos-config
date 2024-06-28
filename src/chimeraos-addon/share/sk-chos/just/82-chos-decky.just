# vim: set ft=make :

# 安装 Decky
decky-install:
    #!/bin/bash
    echo "Installing Decky..."
    curl -sLk https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh | sed 's,#!/bin/sh,#!/bin/sh\nset -e,' | sed 's#| select(.prerelease == "false")##' | sh

# 使用国内镜像安装 Decky
decky-install-cn:
    #!/bin/bash
    echo "Installing Decky..."
    curl -sLk curl -L http://dl.ohmydeck.net | sh