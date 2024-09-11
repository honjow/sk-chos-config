#!/bin/bash

alias_name=cjust

zsh_completions_file_name="_${alias_name}"
bash_completions_file_name="_${alias_name}.bash"

set -e
just --completions zsh > _just
just --completions zsh > $zsh_completions_file_name

sed -i "s/#compdef just/#compdef $alias_name/" $zsh_completions_file_name
sed -i "s/_just/_$alias_name/" $zsh_completions_file_name

just --completions bash > _just.bash
just --completions bash > $bash_completions_file_name

sed -i "s/_just/_$alias_name/" $bash_completions_file_name