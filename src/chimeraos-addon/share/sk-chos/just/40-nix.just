# vim: set ft=make :


# Install the nix package manager / 安装 nix 包管理器
nix-install:
    /usr/bin/sk-nix-install install

# Uninstall the nix package manager / 卸载 nix 包管理器
nix-uninstall:
    /usr/bin/sk-nix-install uninstall