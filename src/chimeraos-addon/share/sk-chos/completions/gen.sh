#!/bin/bash

name=ujust

file_name=_${name}

set -e
just --completions zsh > _just
just --completions zsh > $file_name

sed -i "s/#compdef just/#compdef $name/" $file_name

just --completions bash > _just.bash