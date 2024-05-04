# vim: set ft=make :


# Enable MCU powersave
mcu-powersave-enable:
  #!/usr/bin/bash
  if [ -f /sys/devices/platform/*/mcu_powersave ]; then
    echi 1 | sudo tee /sys/devices/platform/*/mcu_powersave
  fi

# Disable MCU powersave
mcu-powersave-disable:
  #!/usr/bin/bash
  if [ -f /sys/devices/platform/*/mcu_powersave ]; then
    echo 0 | sudo tee /sys/devices/platform/*/mcu_powersave
  fi