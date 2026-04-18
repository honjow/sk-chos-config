#!/bin/bash
# Workaround for AMD APU s2idle/hibernate hang when some CPUs are offline.
# IMPORTANT: CPUs MUST be onlined in ascending NUMERIC order (cpu8 before cpu10),
# not lexicographic order. On at least Strix Halo, low-index CPUs (e.g. cpu8/9)
# fail to come back online if higher-index CPUs are onlined first.

STATE_FILE=/run/cpu-online-suspend.offline
LOG_TAG="cpu-online-suspend"
RETRIES=3
RETRY_DELAY=0.5

set_cpu_state() {
    local online_path=$1
    local target=$2
    local i state
    for ((i=0; i<RETRIES; i++)); do
        echo "$target" > "$online_path" 2>/dev/null
        read -r state < "$online_path" 2>/dev/null || state=
        if [ "$state" = "$target" ]; then
            return 0
        fi
        sleep "$RETRY_DELAY"
    done
    return 1
}

# Collect offline CPU numbers, sorted numerically ascending.
# (Low-index CPUs must be onlined first.)
collect_offline_cpus() {
    local online state cpu
    for online in /sys/devices/system/cpu/cpu*/online; do
        [ -f "$online" ] || continue
        read -r state < "$online" || continue
        [ "$state" = "0" ] || continue
        cpu=${online%/online}
        cpu=${cpu##*/}
        echo "${cpu#cpu}"
    done | sort -n
}

start_ts=$(date +%s.%N)

case "$1" in
    pre)
        : > "$STATE_FILE"
        success=""
        failed=""
        while IFS= read -r n; do
            [ -n "$n" ] || continue
            cpu="cpu$n"
            online_path="/sys/devices/system/cpu/$cpu/online"
            echo "$cpu" >> "$STATE_FILE"
            if set_cpu_state "$online_path" 1; then
                success="$success $cpu"
            else
                failed="$failed $cpu"
            fi
        done < <(collect_offline_cpus)
        end_ts=$(date +%s.%N)
        elapsed=$(awk "BEGIN { printf \"%.2f\", $end_ts - $start_ts }")
        [ -n "$success" ] && logger -t "$LOG_TAG" "onlined for $2 (${elapsed}s):$success"
        [ -n "$failed" ]  && logger -p warning -t "$LOG_TAG" "FAILED to online for $2:$failed (sleep may hang!)"
        ;;
    post)
        if [ -s "$STATE_FILE" ]; then
            success=""
            failed=""
            # Restore offline state. Order on offline path is less critical;
            # use the recorded order (also numerically ascending from pre).
            while IFS= read -r cpu; do
                [ -n "$cpu" ] || continue
                online_path="/sys/devices/system/cpu/$cpu/online"
                [ -f "$online_path" ] || continue
                if set_cpu_state "$online_path" 0; then
                    success="$success $cpu"
                else
                    failed="$failed $cpu"
                fi
            done < "$STATE_FILE"
            end_ts=$(date +%s.%N)
            elapsed=$(awk "BEGIN { printf \"%.2f\", $end_ts - $start_ts }")
            [ -n "$success" ] && logger -t "$LOG_TAG" "restored offline after $2 (${elapsed}s):$success"
            [ -n "$failed" ]  && logger -p warning -t "$LOG_TAG" "FAILED to restore offline after $2:$failed"
        fi
        rm -f "$STATE_FILE"
        ;;
esac
exit 0