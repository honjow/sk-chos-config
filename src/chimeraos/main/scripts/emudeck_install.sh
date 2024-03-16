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

github_release_prefix=$1
github_raw_prefix=$2

echo "github_release_prefix: ${github_release_prefix}"
echo "github_raw_prefix: ${github_raw_prefix}"

tmp_dir=$(mktemp -d)

EMUDECK_GITHUB_URL="https://api.github.com/repos/EmuDeck/emudeck-electron/releases/latest"
RELEASE=$(curl -s ${EMUDECK_GITHUB_URL})

echo "RELEASE $RELEASE"

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

if [[ -n "$github_release_prefix" ]]; then
  # replace 'https://github.com' with the custom prefix
  RELEASE_URL=$(echo $RELEASE_URL | sed "s|https://github.com|${github_release_prefix}|")
  echo "RELEASE_URL: ${RELEASE_URL}"
fi

ICON_URL="https://raw.githubusercontent.com/dragoonDorise/EmuDeck/main/icons/EmuDeck.png"
if [[ -n "$github_raw_prefix" ]]; then
  # replace 'https://raw.githubusercontent.com' with the custom prefix
  ICON_URL=$(echo $ICON_URL | sed "s|https://raw.githubusercontent.com|${github_raw_prefix}|")
  echo "ICON_URL: ${ICON_URL}"
fi

mkdir -p ~/Applications

echo "Downloading icon"
curl -L "${ICON_URL}" -o ${tmp_dir}/EmuDeck.png
cp ${tmp_dir}/EmuDeck.png ~/Applications/EmuDeck.png

echo "Installing EmuDeck $RELEASE_VERSION"

curl -L "${RELEASE_URL}" -o ${tmp_dir}/EmuDeck.AppImage
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