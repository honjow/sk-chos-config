#!/bin/bash

[ "$UID" -eq 0 ] || exec sudo "$0" "$@"

swapfile_path=/frzr_root/swap/swapfile

# swapoff 
swapoff $swapfile_path 2>/dev/null

sk-mkswapfile "$@"

# swapon
swapon $swapfile_path

sk-setup-kernel-options