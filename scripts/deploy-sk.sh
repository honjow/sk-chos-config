#!/bin/bash

set -e

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

src=/frzr_root/deployments
dst=/mnt/sk/deployments

# 首先创建 chimeraos-xxxxxxxx 的只读快照
cd $src
subname=$(ls -t | head -1)

# if ${subname}_r exists, delete it
if [ -d "${subname}_r" ]; then
    btrfs subvolume delete ${subname}_r
fi

btrfs subvolume snapshot -r $subname ${subname}_r

echo "Deploying $subname to $dst"

# 删除旧的子卷
echo "Deleting old deployments..."
cd $dst
btrfs subvolume delete chimeraos-4*_* || true
btrfs filesystem sync $dst

# 发送到指顶路径
echo "Sending $subname to $dst..."
btrfs send --proto 2 --compressed-data $src/${subname}_r | btrfs receive $dst

# 创建为读写子卷
echo "Creating RW subvolume..."
cd $dst && btrfs subvolume snapshot ${subname}_r ${subname}

# 删除只读子卷
echo "Deleting RO subvolume..."
btrfs subvolume delete $dst/${subname}_r
btrfs subvolume delete $src/${subname}_r
