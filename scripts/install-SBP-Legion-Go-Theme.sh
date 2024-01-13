#!/bin/bash

if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as a normal user, not root."
    exit 1
fi

git_url="https://github.com/frazse/SBP-Legion-Go-Theme.git"
commit_id=""

temp_dir=$(mktemp -d)
cd $temp_dir

git clone $git_url
cd SBP-Legion-Go-Theme
if [ "$commit_id" != "" ]; then
    git checkout $commit_id
fi

mkdir -p $HOME/homebrew/themes

if [ -d $HOME/homebrew/themes/SBP-Legion-Go-Theme ]; then
    rm -rf $HOME/homebrew/themes/SBP-Legion-Go-Theme
fi

cp -r $temp_dir/SBP-Legion-Go-Theme $HOME/homebrew/themes