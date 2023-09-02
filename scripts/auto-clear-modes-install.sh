#!/bin/bash

WORKING_FOLDER="${HOME}/.auto-clear-modes"

mkdir -p "${WORKING_FOLDER}"
mkdir -p "${HOME}/.config/systemd/user/"

# Add new service file
cat > "${WORKING_FOLDER}/auto-clear-modes.service" <<- EOF
[Unit]
Description=Auto Clear Modes
After=network.target

[Service]
Type=simple
ExecStart=rm ${HOME}/.config/gamescope/modes.cfg
WorkingDirectory=${WORKING_FOLDER}

[Install]
WantedBy=multi-user.target
EOF

# cp to user systemd folder
cp "${WORKING_FOLDER}/auto-clear-modes.service" "${HOME}/.config/systemd/user/"

# Enable service
systemctl --user daemon-reload
systemctl --user enable auto-clear-modes.service