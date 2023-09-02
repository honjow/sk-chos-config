#!/bin/bash

WORKING_FOLDER="${HOME}/.auto-clear-modes"

# disable service
systemctl --user daemon-reload
systemctl --user disable auto-clear-modes.service

# remove service file
rm "${HOME}/.config/systemd/user/auto-clear-modes.service"