# vim: set ft=make :


# Enable MCU powersave / 开启 MCU 节能模式
mcu-powersave-enable:
    #!/usr/bin/bash
    if [ -f /sys/devices/platform/*/mcu_powersave ]; then
        sudo bash -c "echo 1 > /sys/devices/platform/*/mcu_powersave"
    else
        echo "MCU powersave not supported"
    fi

# Disable MCU powersave / 关闭 MCU 节能模式
mcu-powersave-disable:
    #!/usr/bin/bash
    if [ -f /sys/devices/platform/*/mcu_powersave ]; then
        sudo bash -c "echo 0 > /sys/devices/platform/*/mcu_powersave"
    else
        echo "MCU powersave not supported"
    fi