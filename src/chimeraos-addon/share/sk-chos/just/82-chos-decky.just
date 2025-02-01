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
    curl -L http://dl.ohmydeck.net | sh

decky-framegen:
    #!/bin/bash
    set -e
    echo "Installing Decky-Framegen..."
    github_api_url="https://api.github.com/repos/xXJSONDeruloXx/Decky-Framegen/releases/latest"
    package="Decky-Framegen"
    temp=$(mktemp -d)
    chmod -R +w "${HOME}/homebrew/plugins/"
    plugin_dir="${HOME}/homebrew/plugins/${package}"
    mkdir -p $plugin_dir
    RELEASE=$(curl -s "$github_api_url")
    MESSAGE=$(echo "$RELEASE" | jq -r '.message')
    RELEASE_VERSION=$(echo "$RELEASE" | jq -r '.tag_name')
    RELEASE_URL=$(echo "$RELEASE" | jq -r '.assets[0].browser_download_url')
    temp_file="${temp}/${package}.zip"

    echo "Downloading $package $RELEASE_VERSION"
    curl -L "$RELEASE_URL" -o "$temp_file"

    echo "Unzipping $package $RELEASE_VERSION"
    unzip -o "$temp_file" -d "$plugin_dir"
    sudo rsync -av "${temp}/${package}/" $plugin_dir --delete
    rm -rf "${temp}"
    sudo systemctl restart plugin_loader.service