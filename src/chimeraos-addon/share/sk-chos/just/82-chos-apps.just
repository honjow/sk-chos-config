# vim: set ft=make :


# Install Handheld Daemon / 安装更新 Handheld Daemon
[group("system")]
install-hhd:
    /usr/bin/__hhd-update

# Install frzr / 安装更新 frzr
[group("system")]
install-frzr-sk:
    /usr/bin/__frzr-sk-update

# Install device quirks / 安装设备特殊处理脚本
[group("system")]
install-device-quirks:
    /usr/bin/__device-quirks-update

# Install gamescope session / 更新 gamescope session
[group("system")]
install-gamescope-session:
    /usr/bin/__gamescope-session-update


# Install Adwaita-for-Steam theme for CSS Loader (https://github.com/tkashkin/Adwaita-for-Steam)
[group("gaming")]
install-adwaita-for-steam:
    #!/usr/bin/bash
    if [ -d "$HOME/homebrew/themes" ]; then
        rm -rf "$HOME/homebrew/themes/Adwaita-for-Steam"
        git clone https://github.com/tkashkin/Adwaita-for-Steam.git --single-branch "$HOME/homebrew/themes/Adwaita-for-Steam"
    else
        echo 'Please install Decky Loader first, then install CSS Loader from the Decky Plugin Store.'
    fi