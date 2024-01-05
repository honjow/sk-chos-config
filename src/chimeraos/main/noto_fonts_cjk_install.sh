#!/bin/bash

if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as a normal user, not root."
    exit 1
fi

# acton is install or uninstall
ACTION=$1

function fonts_config() {
    cat > ~/.fonts.conf <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
    <dir>~/.fonts</dir>
</fontconfig>
EOF
    mkdir -p ~/.fonts
}

# function to install the fonts
function install_fonts() {
    # install the fonts
    echo "Installing the Noto CJK fonts..."
    cat > ~/.fonts/60-noto-cjk.conf <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer>
      <family>Noto Sans CJK SC</family>
      <family>Noto Sans CJK TC</family>
      <family>Noto Sans CJK JP</family>
      <family>Noto Sans CJK KR</family>
    </prefer>
  </alias>
  <alias>
    <family>serif</family>
    <prefer>
      <family>Noto Serif CJK SC</family>
      <family>Noto Serif CJK TC</family>
      <family>Noto Serif CJK JP</family>
      <family>Noto Serif CJK KR</family>
    </prefer>
  </alias>
  <alias>
    <family>monospace</family>
    <prefer>
      <family>Noto Sans Mono CJK SC</family>
      <family>Noto Sans Mono CJK TC</family>
      <family>Noto Sans Mono CJK JP</family>
      <family>Noto Sans Mono CJK KR</family>
    </prefer>
  </alias>
</fontconfig>
EOF
    sudo pacman -Sy --noconfirm --needed noto-fonts-cjk && \
    cp -r /usr/share/fonts/noto-cjk ~/.fonts/ && \
    sudo pacman -R --noconfirm noto-fonts-cjk
    # refresh the font cache
    fc-cache -fv
    echo "Done."
}

# function to uninstall the fonts
function uninstall_fonts() {
    # uninstall the fonts
    echo "Uninstalling the Noto CJK fonts..."
    
    rm -f ~/.fonts/60-noto-cjk.conf
    rm -rf ~/.fonts/noto-cjk
    # refresh the font cache
    fc-cache -fv
    echo "Done."
}


fonts_config

# case install or uninstall
case "$ACTION" in
    install)
        install_fonts
        ;;
    uninstall)
        uninstall_fonts
        ;;
    *)
        echo "Usage: $0 [install|uninstall]"
        exit 1
        ;;
esac