#!/bin/bash

if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as a normal user, not root."
    exit 1
fi

theme_name="PS5-to-Xbox-glyphs"

git_url="https://github.com/frazse/PS5-to-Xbox-glyphs.git"
commit_id=""

temp_dir=$(mktemp -d)
cd $temp_dir

git clone $git_url
cd $theme_name
if [ "$commit_id" != "" ]; then
    git checkout $commit_id
fi

mkdir -p $HOME/homebrew/themes

if [ -d $HOME/homebrew/themes/$theme_name ]; then
    rm -rf $HOME/homebrew/themes/$theme_name
fi

cp -r $temp_dir/$theme_name $HOME/homebrew/themes