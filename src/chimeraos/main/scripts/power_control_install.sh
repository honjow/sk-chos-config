#!/bin/bash

# check if jq is installed
if ! [ -x "$(command -v jq)" ]; then
  echo 'Error: jq is not installed.' >&2
  exit 1
fi

set -e

github_release_prefix=$1
echo "github_release_prefix: ${github_release_prefix}"

temp=$(mktemp -d)

# Download latest release
RELEASE=$(curl -s "https://api.github.com/repos/mengmeet/PowerControl/releases/latest" --connect-timeout 10)

MESSAGE=$(echo "$RELEASE" | jq -r '.message')

if [[ "$MESSAGE" != "null" ]]; then
  echo "$MESSAGE" >&2
  exit 1
fi

RELEASE_VERSION=$(echo "$RELEASE" | jq -r '.tag_name')
RELEASE_URL=$(echo "$RELEASE" | jq -r '.assets[0].browser_download_url')

if [ -z "$RELEASE_VERSION" ] || [ -z "$RELEASE_URL" ]; then
  echo "Failed to get latest release info" >&2
  exit 1
fi

if [[ -n "$github_release_prefix" ]]; then
  # replace 'https://github.com' with the custom prefix
  RELEASE_URL=$(echo $RELEASE_URL | sed "s|https://github.com|${github_release_prefix}|")
  echo "RELEASE_URL: ${RELEASE_URL}"
fi

curl -L -o ${temp}/PowerControl.tar.gz "${RELEASE_URL}" --connect-timeout 10 -m 120

echo "Installing PowerControl $RELEASE_VERSION"

if [ ! -f ${temp}/PowerControl.tar.gz ]; then
  echo "Failed to download PowerControl $RELEASE_VERSION" >&2
  exit 1
fi

# remove old version
sudo chmod -R 777 ${HOME}/homebrew/plugins
sudo rm -rf ${HOME}/homebrew/plugins/PowerControl

# Extract
tar -xzf ${temp}/PowerControl.tar.gz -C ${HOME}/homebrew/plugins

# Cleanup
rm -f ${temp}/PowerControl.tar.gz

echo "PowerControl $RELEASE_VERSION installed"

# restart plugin_loader
sudo systemctl restart plugin_loader.service
