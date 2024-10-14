#!/bin/bash

set -e

STATE_FILE="/tmp/.deckyplumber.state"

# 哨兵文件
SENTINEL_FILE="/tmp/.deckyplumber.deck.sentinel"

function pre_suspend() {
    if lsusb | grep 'Valve Software Steam Controller' >/dev/null; then
        echo "Steam Controller detected, disconnect all virtual devices"
        busctl call org.shadowblip.InputPlumber \
            /org/shadowblip/InputPlumber/CompositeDevice0 \
            org.shadowblip.Input.CompositeDevice \
            SetTargetDevices as 0

        for i in $(seq 1 10); do
            if [[ $(busctl get-property org.shadowblip.InputPlumber \
                /org/shadowblip/InputPlumber/CompositeDevice0 \
                org.shadowblip.Input.CompositeDevice \
                TargetDevices | grep -o 'as 0' | wc -l) -eq 1 ]]; then
                break
            fi
            sleep 1
        done

        sleep 2

        echo "Disconnecting all virtual devices done"
        touch $SENTINEL_FILE
    fi

}

function post_resume() {
    STATE=$(cat $STATE_FILE)
    if [[ -f $SENTINEL_FILE || "$STATE" == "deck" ]]; then
        echo "Reconnect all virtual devices"
        busctl call org.shadowblip.InputPlumber \
            /org/shadowblip/InputPlumber/CompositeDevice0 \
            org.shadowblip.Input.CompositeDevice \
            SetTargetDevices as 3 deck keyboard mouse
        echo "Reconnecting deck virtual devices done"
        if [[ -f $SENTINEL_FILE ]]; then
            rm $SENTINEL_FILE
        fi
    fi

}

case $1 in
pre)
    pre_suspend
    ;;
post)
    post_resume
    ;;
esac
