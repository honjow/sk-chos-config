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

app_name="sleepy-launcher"
entry_name="Sleepy Launcher"

tmp_dir=$(mktemp -d)

EMUDECK_GITHUB_URL="https://api.github.com/repos/an-anime-team/${app_name}/releases/latest"
RELEASE=$(curl -s ${EMUDECK_GITHUB_URL} --connect-timeout 10)

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

ICON_URL="https://raw.githubusercontent.com/an-anime-team/${app_name}/main/assets/images/icon.png"
ICON_URL_CN="https://gitee.com/honjow/sk-holoiso-config/raw/master/assets/icons/${app_name}.png"
if [[ -n "$github_raw_prefix" ]]; then
  # replace 'https://raw.githubusercontent.com' with the custom prefix
  ICON_URL=$(echo $ICON_URL | sed "s|https://raw.githubusercontent.com|${github_raw_prefix}|")
  echo "ICON_URL: ${ICON_URL}"
fi

mkdir -p "$HOME/Applications"

echo "Downloading icon ......"
icon_path="${tmp_dir}/${app_name}.png"
curl -L "${ICON_URL}" -o ${icon_path} --connect-timeout 10 -m 30
# if iconfile is text, then it's an error
if [[ $(file --mime-type -b ${icon_path}) =~ "text" ]]; then
  echo ">>> Failed to download icon, trying gitee source"
  curl -L "${ICON_URL_CN}" -o ${icon_path} --connect-timeout 10 -m 30
fi
cp -f ${icon_path} "$HOME/Applications/${app_name}.png"

echo "Downloading AppImage ......"
temp_appimage="${tmp_dir}/${app_name}.AppImage"
curl -L "${RELEASE_URL}" -o $temp_appimage --connect-timeout 10

# check file type
if [[ ! $(file --mime-type -b $temp_appimage) =~ "application/x" ]]; then
  echo "Failed to download AppImage" >&2
  exit 1
fi

echo "Installing ${app_name} $RELEASE_VERSION"
mv $temp_appimage "$HOME/Applications/${app_name}.AppImage"
chmod +x "$HOME/Applications/${app_name}.AppImage"


user_home=$(eval echo ~${SUDO_USER})

echo "Creating desktop shortcut"
cat > ${user_home}/.local/share/applications/${app_name}.desktop <<EOL
[Desktop Entry]
Name=${entry_name}
Exec=${user_home}/Applications/${app_name}.AppImage
Icon=${user_home}/Applications/${app_name}.png
Terminal=false
Type=Application
Categories=Game;
Keywords=game;
Keywords=sl
EOL