#!/bin/bash
set -e
just --completions zsh > _just.zsh
just --completions zsh > _skjust.zsh

sed -i 's/#compdef just/#compdef skjust/' _skjust.zsh

just --completions bash > _just.bash