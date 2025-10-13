# vim: set ft=make :

# from https://github.com/ublue-os/bazzite/blob/main/system_files/desktop/shared/usr/share/ublue-os/just/82-bazzite-waydroid.just

alias configure-waydroid := setup-waydroid

# Launch Waydroid configuration helper
setup-waydroid ACTION="":
    #!/usr/bin/bash
    set -eu
    source /usr/lib/cjust/cjust.sh
    OPTION={{ ACTION }}
    if [ "$OPTION" == "help" ]; then
      echo "Usage: cjust configure-waydroid <option>"
      echo "  <option>: Specify the quick option to skip the prompt / 快速设置选项"
      echo "  Use 'init' to select Initialize Waydroid / 初始化 Waydroid"
      echo "  Use 'configure' to select Configure Waydroid / 配置 Waydroid"
      echo "  Use 'gpu' to choose Select GPU for Waydroid / 选择 GPU"
      echo "  Use 'libhoudini' to install Libhoudini for Waydroid / 安装 Libhoudini"
      echo "  Use 'integration' to toggle desktop window integration for Waydroid / 切换 Waydroid 的桌面窗口集成"
      echo "  Use 'reset' to select Configure Waydroid / 重置 Waydroid"
      echo "  Use 'add-to-steam' to add Waydroid to Steam / 添加 Waydroid 到 Steam"
      echo "  Use 'exit' to exit / 退出"
      exit 0
    elif [ "$OPTION" == "" ]; then
      echo "${bold}Waydroid Setup${normal}"
      OPTION=$(Choose \
        "Initialize Waydroid / 初始化Waydroid" \
        "Configure Waydroid / 配置Waydroid" \
        "Select GPU for Waydroid / 选择 GPU" \
        "Libhoudini for Waydroid / 安装 Libhoudini" \
        "Toggle Desktop Window Integration / 切换桌面窗口集成" \
        "Reset Waydroid / 重置 Waydroid" \
        "Add Waydroid to Steam / 添加 Waydroid 到 Steam (会重启 Steam)" \
        "Exit / 退出" \
        )
    fi
    if [[ "${OPTION,,}" =~ ^exit ]]; then
      exit 0
    elif [[ "${OPTION,,}" =~ ^init ]]; then
      sudo waydroid init -f -s GAPPS
      sudo waydroid-extras install libhoudini
      echo "Waydroid has been initialized, please run waydroid once before you Configure Waydroid"
    elif [[ "${OPTION,,}" =~ ^configure ]]; then
      sudo /usr/bin/waydroid-extras
    elif [[ "${OPTION,,}" =~ gpu ]]; then
      sudo /usr/bin/waydroid-choose-gpu
    elif [[ "${OPTION,,}" =~ libhoudini ]]; then
      sudo waydroid-extras install libhoudini
    elif [[ "${OPTION,,}" =~ integration ]]; then
      current=$(waydroid prop get persist.waydroid.multi_windows)
      if [[ "$current" == "true" ]]; then
        waydroid prop set persist.waydroid.multi_windows false
        echo "Waydroid Desktop Window Integration has been disabled"
      else
        waydroid prop set persist.waydroid.multi_windows true
        echo "Waydroid Desktop Window Integration has been enabled"
      fi
    elif [[ "${OPTION,,}" =~ ^reset ]]; then
      echo "Resetting Waydroid"
      sudo rm -rf /var/lib/waydroid /home/.waydroid ~/waydroid ~/.share/waydroid ~/.local/share/applications/*aydroid* ~/.local/share/waydroid
      echo "Waydroid has been reset"
    elif [[ "${OPTION,,}" =~ ^add ]]; then
      name="Waydroid"
      exe='"/usr/bin/waydroid-launcher"'

      function steam_shortcuts_setimg() {
        # 设置封面图片 并重启 Steam
        local name="$1"
        local exe="$2"
        local exec_when_done="${3:-pkill -f steam -HUP}"
        steam_shortcuts -t setimg -n "$name" -e "$exe" \
          --icon "/usr/share/applications/Waydroid/icon.png" \
          --cover "/usr/share/applications/Waydroid/capsule.png" \
          --banner "/usr/share/applications/Waydroid/store-capsule.png" \
          --background "/usr/share/applications/Waydroid/hero.png" \
          --logo "/usr/share/applications/Waydroid/logo.png" && \
          eval "$exec_when_done"
      }

      # 检查是否已经添加到 Steam
      if steam_shortcuts -t isexisted -n "$name" -e "$exe"; then
        echo "Waydroid is already added to Steam"
      else
        /usr/bin/steamos-add-to-steam /usr/share/applications/Waydroid.desktop
        echo "Waydroid added to Steam done"
        sleep 2
        steam_shortcuts_setimg "$name" "$exe"
        exit 0
      fi

      # 设置封面图片
      if steam_shortcuts -t isexisted -n "$name" -e "$exe"; then
        steam_shortcuts_setimg "$name" "$exe" "echo 'Waydroid added to Steam done'"
      fi
    fi
