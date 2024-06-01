# vim: set ft=make :

# some from https://github.com/ublue-os/config/blob/main/build/ublue-os-just/00-default.just

uid := `id -u`
shell := `grep :$(id -u): /etc/passwd | cut -d: -f7`

alias logs-flower := logs-this-boot-flower

# Boot into this device's BIOS/UEFI screen / 重启进入 BIOS/UEFI 界面
bios:
    #!/usr/bin/bash
    if [ -d /sys/firmware/efi ]; then
      sudo systemctl reboot --firmware-setup
    else
      echo "Rebooting to legacy BIOS from OS is not supported."
    fi

# Boot to Universal AMD Form Browser / 重启进入通用 AMD BIOS/UEFI 界面
boot-umaf:
    sudo /usr/libexec/boot-umaf

# Boot to EFI Shell / 重启进入 EFI Shell
boot-efi-shell:
    sudo /usr/libexec/boot-efi-shell

# Show all messages from this boot / 显示本次启动的所有日志
logs-this-boot:
    sudo journalctl -b 0

# Show all messages from this boot, and keep updating / 显示本次启动的所有日志，并持续更新
logs-this-boot-flower:
    sudo journalctl -b 0 -f

# Show all messages from last boot / 显示上次启动的所有日志
logs-last-boot:
    sudo journalctl -b -1

# Change the user's shell / 更改用户的 shell
chsh new_shell:
    #!/usr/bin/bash
    set -euo pipefail
    if [ "{{ shell }}" = "{{ new_shell }}" ] ; then
      printf "Your shell is already set to %s.\n" "{{ new_shell }}"
    else
      if [ -x "{{ new_shell }}" ] ; then
        sudo usermod $USER --shell "{{ new_shell }}"
        printf "%s's shell is now %s.\n" "$USER" "{{ new_shell }}"
      else
        echo "{{ new_shell }} does not exist or is not executable!"
      fi
    fi

# Gather device info to a pastebin / 收集设备信息到 pastebin
device-info:
    #!/usr/bin/bash
    echo "Gathering device info..."
    fpaste <(fpaste --sysinfo --printonly)


# Toggle display of the user-motd in terminal / 切换终端中是否显示信息
toggle-user-motd:
    #!/usr/bin/bash
    if test -e "${HOME}/.config/no-show-user-motd"; then
      rm -f "${HOME}/.config/no-show-user-motd"
    else
      if test ! -d "${HOME}/.config"; then
        mkdir "${HOME}/.config"
      fi
      touch "${HOME}/.config/no-show-user-motd"
    fi

# Test amd s2idle suspend / 测试 amd s2idle 睡眠
amd-s2idle-test:
    #!/usr/bin/bash
    if [ -x $(command -v amd_s2idle-analysis) ]; then
      sudo amd_s2idle-analysis --force --log "s2idle_report_$(date +%Y%m%d_%H%M%S).log"
    else
      echo "amd_s2idle-analysis is not installed."
    fi

# Show battery information / 显示电池信息
battery-info:
    #!/usr/bin/bash
    battery=$(upower -e | grep 'BAT')
    if [ -x $(command -v upower) ]; then
      upower -i $battery
    else
      echo "upower is not installed."
    fi