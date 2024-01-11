#!/bin/bash

if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as a normal user, not root."
    exit 1
fi

git_url="https://github.com/semakusut/SBP-ROG-Ally.git"
commit_id="fd803c1bb95eedf98df749460d96e980de3d45d2"

temp_dir=$(mktemp -d)
cd $temp_dir

git clone $git_url
cd SBP-ROG-Ally
if [ "$commit_id" != "" ]; then
    git checkout $commit_id
fi

# Install SBP-ROG-Ally
mkdir -p $HOME/homebrew/themes

if [ -d $HOME/homebrew/themes/SBP-ROG-Ally ]; then
    rm -rf $HOME/homebrew/themes/SBP-ROG-Ally
fi

cp -r $temp_dir/SBP-ROG-Ally $HOME/homebrew/themes