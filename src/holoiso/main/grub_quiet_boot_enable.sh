#!/bin/bash
echo "quiet" | sudo tee /etc/default/grub_quiet
sudo update-grub