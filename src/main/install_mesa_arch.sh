#!/bin/bash
sudo pacman --config /etc/arch_pacman.conf --noconfirm -Sy \
llvm llvm-libs lib32-llvm-libs \
mesa libva-mesa-driver mesa-utils mesa-vdpau opencl-mesa vulkan-intel vulkan-radeon \
lib32-mesa lib32-libva-mesa-driver lib32-mesa-vdpau lib32-vulkan-intel lib32-vulkan-radeon

sudo pacman -Syy --noconfirm