#!/usr/bin/python
# coding=utf-8

import subprocess

def get_product_name():
    # get from /sys/devices/virtual/dmi/id/product_name
    product_name = ""
    try:
        with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
            product_name = f.readline().strip()
    except Exception as e:
        print("读取设备名称失败:", str(e))
    return product_name

# 执行命令
def run_command(command, name=""):
    success = True
    ret_msg = ""
    print(f"执行{name}更新操作")
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in process.stdout:
            print(line.strip())
        stdout, stderr = process.communicate()
        return_code = process.returncode

        if return_code != 0:
            success = False
            ret_msg = stderr.decode().strip()
            print(f"{name}更新失败: {ret_msg}")
        else:
            print(f"{name}更新完成")
    except Exception as e:
        success = False
        ret_msg = str(e)
        print(f"{name}更新失败: {ret_msg}")
    
    return success, ret_msg

# 检查服务是否已启用
def check_service_autostart(service_name):
    try:
        output = subprocess.check_output(['sudo', 'systemctl', 'is-enabled', service_name]).decode().strip()
        return output == 'enabled'
    except subprocess.CalledProcessError:
        # 如果命令执行出错，则服务可能不存在或无法访问
        return False

def toggle_service(service_name, enable):
    action = "enable" if enable else "disable"
    try:
        sudo_cmd = ['sudo', 'systemctl', action, '--now', service_name]
        subprocess.run(sudo_cmd, check=True)
        print(f"服务 {service_name} {action}成功")
    except subprocess.CalledProcessError as e:
        print(f"服务 {service_name} {action}失败:", str(e))