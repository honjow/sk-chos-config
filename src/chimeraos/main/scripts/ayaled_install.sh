#!/bin/bash

# check if jq is installed
if ! [ -x "$(command -v jq)" ]; then
  echo 'Error: jq is not installed.' >&2
  exit 1
fi

set -e

github_prefix=$1
echo "github_prefix: ${github_prefix}"

temp=$(mktemp -d)

# Download latest release
RELEASE=$(curl -s "${github_prefix}https://api.github.com/repos/honjow/ayaled/releases/latest")

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

curl -L -o ${temp}/ayaled.tar.gz "${github_prefix}${RELEASE_URL}"

echo "Installing ayaled $RELEASE_VERSION"

if [ ! -f ${temp}/ayaled.tar.gz ]; then
  echo "Failed to download ayaled $RELEASE_VERSION" >&2
  exit 1
fi

# remove old version
chmod -R 777 ${HOME}/homebrew/plugins
rm -rf ${HOME}/homebrew/plugins/ayaled

# Extract
tar -xzf ${temp}/ayaled.tar.gz -C ${HOME}/homebrew/plugins

# Cleanup
rm -f ${temp}/ayaled.tar.gz

echo "ayaled $RELEASE_VERSION installed"

# restart plugin_loader
sudo systemctl restart plugin_loader.service
