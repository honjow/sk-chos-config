# vim: set ft=make :


# Enable MCU powersave / 开启 MCU 节能模式
_mcu-powersave-enable:
    #!/usr/bin/bash
    if [ -f /sys/devices/platform/*/mcu_powersave ]; then
        sudo bash -c "echo 1 > /sys/devices/platform/*/mcu_powersave"
    elif [ -f /sys/class/firmware-attributes/asus-armoury/attributes/mcu_powersave/current_value ]; then
        sudo bash -c "echo 1 > /sys/class/firmware-attributes/asus-armoury/attributes/mcu_powersave/current_value"
    else
        echo "MCU powersave not supported"
    fi

# Disable MCU powersave / 关闭 MCU 节能模式
_mcu-powersave-disable:
    #!/usr/bin/bash
    if [ -f /sys/devices/platform/*/mcu_powersave ]; then
        sudo bash -c "echo 0 > /sys/devices/platform/*/mcu_powersave"
    elif [ -f /sys/class/firmware-attributes/asus-armoury/attributes/mcu_powersave/current_value ]; then
        sudo bash -c "echo 0 > /sys/class/firmware-attributes/asus-armoury/attributes/mcu_powersave/current_value"
    else
        echo "MCU powersave not supported"
    fi