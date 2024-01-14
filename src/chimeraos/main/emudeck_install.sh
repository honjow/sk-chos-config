#!/bin/bash

# cant run this script as root
if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as a normal user, not root."
    exit 1
fi

# check if jq is installed
if ! [ -x "$(command -v jq)" ]; then
  echo 'Error: jq is not installed.' >&2
  exit 1
fi

set -e

github_prefix=$1
echo "github_prefix: ${github_prefix}"

tmp_dir=$(mktemp -d)


EMUDECK_GITHUB_URL="https://api.github.com/repos/EmuDeck/emudeck-electron/releases/latest"
RELEASE=$(curl -s ${github_prefix}${EMUDECK_GITHUB_URL})

# echo "RELEASE $RELEASE"

MESSAGE=$(echo "$RELEASE" | jq -r '.message')

# if MESSAGE not null, then there is an error
if [[ "x$MESSAGE" != "xnull" ]]; then
  echo -e "Failed to get latest release info:\n${MESSAGE}" >&2
  exit 1
fi

RELEASE_VERSION=$(echo "$RELEASE" | jq -r '.tag_name')
RELEASE_URL=$(echo "$RELEASE" | jq -r '.assets[0].browser_download_url')

echo "RELEASE_VERSION: ${RELEASE_VERSION}"
echo "RELEASE_URL: ${RELEASE_URL}"

if [ -z "$RELEASE_VERSION" ] || [ -z "$RELEASE_URL" ]; then
  echo "Failed to get latest release info" >&2
  exit 1
fi

ICON_URL="https://github.com/dragoonDorise/EmuDeck/blob/main/icons/EmuDeck.png?raw=true"

echo "Downloading icon"
curl -L "${github_prefix}${ICON_URL}" -o ${tmp_dir}/EmuDeck.png
cp ${tmp_dir}/EmuDeck.png ~/Applications/EmuDeck.png

echo "Installing EmuDeck $RELEASE_VERSION"

mkdir -p ~/Applications
curl -L "${github_prefix}${RELEASE_URL}" -o ${tmp_dir}/EmuDeck.AppImage
mv ${tmp_dir}/EmuDeck.AppImage ~/Applications/EmuDeck.AppImage
chmod +x ~/Applications/EmuDeck.AppImage


user_home=$(eval echo ~${SUDO_USER})

echo "Creating desktop shortcut"
cat > ${user_home}/.local/share/applications/EmuDeck.desktop <<EOL
[Desktop Entry]
Name=EmuDeck
Exec=${user_home}/Applications/EmuDeck.AppImage
Icon=${user_home}/Applications/EmuDeck.png
Terminal=false
Type=Application
Categories=Gaming;Application;
EOL