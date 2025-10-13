# vim: set ft=make :

# Credit: https://github.com/ublue-os/bazzite/pull/3194/files

# Configure auto-pause on suspend/resume for running games. Can fix audio crackling on wake. May cause problems with some games. Check out Pause Games Decky plugin for finer control. / 配置自动暂停在挂起/恢复时运行游戏。可以修复唤醒时的音频爆裂问题。可能会对某些游戏造成问题。查看 Pause Games Decky 插件以进行更精细的控制。
[group("gaming")]
setup-auto-pause ACTION="":
    #!/usr/bin/bash
    source /usr/lib/cjust/cjust.sh
    SERVICE_FILE="$HOME/.config/systemd/user/auto-pause.service"

    if systemctl --user is-enabled auto-pause.service &>/dev/null; then
      echo "Current status: ${green}${bold}enabled${normal}"
      CHOICE=$(ugum choose "Disable auto-pause / 禁用自动暂停" "Exit without changes / 不更改并退出")
      if [[ "$CHOICE" == "Disable auto-pause" ]]; then
        systemctl --user disable --now auto-pause.service 2>/dev/null || true
        rm -f "$SERVICE_FILE"
        systemctl --user daemon-reload
        echo "Auto-pause service ${red}${bold}disabled${normal} and service file removed."
      else
        echo "No changes made."
      fi
    else
      echo "Current status: ${red}${bold}disabled${normal}"
      CHOICE=$(ugum choose "Enable auto-pause / 启用自动暂停" "Exit without changes / 不更改并退出")
      if [[ "$CHOICE" == "Enable auto-pause" ]]; then
        mkdir -p "$(dirname "$SERVICE_FILE")"
        {
          echo "[Unit]"
          echo "Description=Auto-Pause Service"
          echo "After=graphical-session.target"
          echo ""
          echo "[Service]"
          echo "Type=simple"
          echo "ExecStart=/usr/libexec/auto-pause-daemon"
          echo "Restart=on-failure"
          echo "RestartSec=5"
          echo ""
          echo "[Install]"
          echo "WantedBy=default.target"
        } > "$SERVICE_FILE"
        systemctl --user daemon-reload
        systemctl --user enable --now auto-pause.service
        echo "Auto-pause service ${green}${bold}enabled${normal}."
        echo "Games will now automatically pause before system suspend and resume after wake."
      else
        echo "No changes made."
      fi
    fi