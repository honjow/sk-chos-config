#!/bin/bash
sudo pacman --config /etc/valve_main_pacman.conf --noconfirm -Syy \
mesa libva-mesa-driver mesa-utils mesa-vdpau opencl-mesa vulkan-intel vulkan-radeon \
lib32-mesa lib32-libva-mesa-driver lib32-mesa-vdpau lib32-vulkan-intel lib32-vulkan-radeon

sudo pacman -Syy --noconfirm