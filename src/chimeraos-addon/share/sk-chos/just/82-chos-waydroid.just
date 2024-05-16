# vim: set ft=make :

# from https://github.com/ublue-os/bazzite/blob/main/system_files/desktop/shared/usr/share/ublue-os/just/82-bazzite-waydroid.just

alias configure-waydroid := setup-waydroid

# Launch Waydroid configuration helper
setup-waydroid ACTION="":
    #!/usr/bin/bash
    source /usr/lib/cjust/cjust.sh
    OPTION={{ ACTION }}
    if [ "$OPTION" == "help" ]; then
      echo "Usage: cjust configure-waydroid <option>"
      echo "  <option>: Specify the quick option to skip the prompt / 快速设置选项"
      echo "  Use 'init' to select Initialize Waydroid / 初始化 Waydroid"
      echo "  Use 'configure' to select Configure Waydroid / 配置 Waydroid"
      echo "  Use 'gpu' to choose Select GPU for Waydroid / 选择 GPU"
      echo "  Use 'reset' to select Configure Waydroid / 重置 Waydroid"
      echo "  Use 'add-to-steam' to add Waydroid to Steam / 添加 Waydroid 到 Steam"
      exit 0
    elif [ "$OPTION" == "" ]; then
      echo "${bold}Waydroid Setup${normal}"
      OPTION=$(Choose "Initialize Waydroid / 初始化Waydroid" "Configure Waydroid / 配置Waydroid" "Select GPU for Waydroid / 选择 GPU" "Reset Waydroid / 重置 Waydroid" "Add Waydroid to Steam / 添加 Waydroid 到 Steam" )
    fi
    if [[ "${OPTION,,}" =~ ^init ]]; then
      sudo waydroid init -c 'https://ota.waydro.id/system' -v 'https://ota.waydro.id/vendor'
      sudo waydroid-extras install libhoudini
      echo "Waydroid has been initialized, please run waydroid once before you Configure Waydroid"
    elif [[ "${OPTION,,}" =~ ^configure ]]; then
      sudo /usr/bin/waydroid-extras
    elif [[ "${OPTION,,}" =~ gpu ]]; then
      /usr/bin/waydroid-choose-gpu
    elif [[ "${OPTION,,}" =~ ^reset ]]; then
      echo "Resetting Waydroid"
      bash -c 'sudo rm -rf /var/lib/waydroid /home/.waydroid ~/waydroid ~/.share/waydroid ~/.local/share/applications/*aydroid* ~/.local/share/waydroid'
      echo "Waydroid has been reset"
    elif [[ "${OPTION,,}" =~ ^add ]]; then
      if steam_shortcuts -t isexisted -n "Waydroid" -e "\"/usr/bin/waydroid-launcher\""; then
        echo "Waydroid is already added to Steam"
      else
        /usr/bin/steamos-add-to-steam /usr/share/applications/Waydroid.desktop
        echo "Waydroid has been added to Steam"
      fi
      steam_shortcuts -t setimg -n "Waydroid" -e "\"/usr/bin/waydroid-launcher\"" \
        --icon "/usr/share/applications/Waydroid/icon.png" \
        --cover "/usr/share/applications/Waydroid/capsule.png" \
        --banner "/usr/share/applications/Waydroid/store-capsule.png" \
        --background "/usr/share/applications/Waydroid/hero.jpg" \
        --logo "/usr/share/applications/Waydroid/logo.png"
      pkill -HUP steam
    fi
