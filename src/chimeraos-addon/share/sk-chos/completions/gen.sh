#!/bin/bash

name=cjust

file_name=_${name}.zsh

set -e
just --completions zsh > _just.zsh
just --completions zsh > $file_name

sed -i "s/#compdef just/#compdef $name/" $file_name

just --completions bash > _just.bash