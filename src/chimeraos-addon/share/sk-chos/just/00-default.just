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