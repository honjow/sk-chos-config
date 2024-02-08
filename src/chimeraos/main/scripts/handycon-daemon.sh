#!/bin/bash

SERVICE_NAME="handycon.service"

while true; do
    # 检查服务 B 是否启用
    if systemctl is-enabled $SERVICE_NAME; then
        # 检查服务 B 的状态
        systemctl is-active $SERVICE_NAME || {
            # 如果服务 B 未激活（启动失败），则重启服务 B
            systemctl restart $SERVICE_NAME
            sleep 5  # 可选：添加一些延迟，以避免立即重试
        }
    else
        echo "Service B is not enabled. Please enable it first."
    fi

    sleep 60  # 每分钟检查一次
done