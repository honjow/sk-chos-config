#!/bin/bash
# Workaround for AMD APU s2idle/hibernate hang when some CPUs are offline.
# Before suspend: record current offline CPUs, then online them all.
# After resume:   restore previously offline CPUs.

STATE_FILE=/run/cpu-online-suspend.offline
LOG_TAG="cpu-online-suspend"

case "$1" in
    pre)
        : > "$STATE_FILE"
        for online in /sys/devices/system/cpu/cpu*/online; do
            [ -f "$online" ] || continue
            read -r state < "$online" || continue
            if [ "$state" = "0" ]; then
                cpu=${online%/online}
                cpu=${cpu##*/}
                echo "$cpu" >> "$STATE_FILE"
                echo 1 > "$online" 2>/dev/null || true
            fi
        done
        if [ -s "$STATE_FILE" ]; then
            logger -t "$LOG_TAG" "onlined for $2: $(tr "\n" " " < "$STATE_FILE")"
        fi
        ;;
    post)
        if [ -s "$STATE_FILE" ]; then
            while IFS= read -r cpu; do
                [ -n "$cpu" ] || continue
                echo 0 > "/sys/devices/system/cpu/$cpu/online" 2>/dev/null || true
            done < "$STATE_FILE"
            logger -t "$LOG_TAG" "restored offline after $2: $(tr "\n" " " < "$STATE_FILE")"
        fi
        rm -f "$STATE_FILE"
        ;;
esac
exit 0