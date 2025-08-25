#!/bin/bash

# SkorionOS Fastfetch Wrapper Installation Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing SkorionOS fastfetch wrapper..."

# 1. Install logo file
echo "Installing logo file..."
sudo mkdir -p /usr/share/fastfetch/logos
sudo cp "$SCRIPT_DIR/skorionos.txt" /usr/share/fastfetch/logos/skorionos.txt
echo "✅ Logo installed: /usr/share/fastfetch/logos/skorionos.txt"

# 2. Install config as preset (not system default)
echo "Installing config preset..."
sudo mkdir -p /usr/share/fastfetch/presets
sudo cp "$SCRIPT_DIR/config.jsonc" /usr/share/fastfetch/presets/skorionos.jsonc
echo "✅ Config preset installed: /usr/share/fastfetch/presets/skorionos.jsonc"

# 3. Backup original fastfetch binary
if [[ ! -f /usr/bin/fastfetch.orig ]]; then
    echo "Backing up original fastfetch..."
    sudo cp /usr/bin/fastfetch /usr/bin/fastfetch.orig
    echo "✅ Original fastfetch backed up: /usr/bin/fastfetch.orig"
else
    echo "ℹ️  Original fastfetch already backed up"
fi

# 4. Install wrapper script
echo "Installing wrapper script..."
sudo cp "$SCRIPT_DIR/fastfetch-wrapper.sh" /usr/bin/fastfetch
sudo chmod +x /usr/bin/fastfetch
echo "✅ Wrapper script installed: /usr/bin/fastfetch"

echo ""
echo "🎉 SkorionOS fastfetch wrapper installed successfully!"
echo ""
echo "Usage:"
echo "  fastfetch                    # Automatically uses SkorionOS logo"
echo "  fastfetch --logo macos       # Uses macos logo (wrapper passes through)"
echo "  fastfetch --config neofetch  # Uses neofetch preset (wrapper passes through)"
echo ""
echo "To uninstall:"
echo "  sudo mv /usr/bin/fastfetch.orig /usr/bin/fastfetch"
