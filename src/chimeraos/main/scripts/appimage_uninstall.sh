#!/bin/bash

# cant run this script as root
if [ "$EUID" -eq 0 ]; then
  echo "Please run this script as a normal user, not root."
  exit 1
fi

set -e

app_name=$1
if [ -z "$app_name" ]; then
  echo "Usage: $0 <appimage_name>"
  exit 1
fi

appimage="$HOME/Applications/${app_name}.AppImage"
icon="$HOME/Applications/${app_name}.png"
desktop="$HOME/.local/share/applications/${app_name}.desktop"

if [ -f "$appimage" ]; then
  rm -f "$appimage"
fi

if [ -f "$icon" ]; then
  rm -f "$icon"
fi

if [ -f "$desktop" ]; then
  rm -f "$desktop"
fi

echo "Uninstall $app_name successfully."

# flush desktop cache
if [ -x "$(command -v xdg-desktop-menu)" ]; then
  xdg-desktop-menu forceupdate
fi
