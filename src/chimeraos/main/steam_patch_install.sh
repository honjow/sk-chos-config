#!/bin/bash
yay -Syy ryzenadj-git jq --needed --noconfirm && \
curl -L https://github.com/honjow/steam-patch/releases/latest/download/install.sh | sh
