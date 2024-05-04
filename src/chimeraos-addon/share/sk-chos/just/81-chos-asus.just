# vim: set ft=make :


# Enable MCU powersave / 开启 MCU 省电模式
mcu-powersave-enable:
    #!/usr/bin/bash
    if [ -f /sys/devices/platform/*/mcu_powersave ]; then
        echi 1 | sudo tee /sys/devices/platform/*/mcu_powersave
    else
        echo "MCU powersave not supported"
    fi

# Disable MCU powersave / 关闭 MCU 省电模式
mcu-powersave-disable:
    #!/usr/bin/bash
    if [ -f /sys/devices/platform/*/mcu_powersave ]; then
        echo 0 | sudo tee /sys/devices/platform/*/mcu_powersave
    else
        echo "MCU powersave not supported"
    fi