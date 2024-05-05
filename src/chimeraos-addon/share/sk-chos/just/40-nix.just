# vim: set ft=make :


# Install the nix package manager / 安装 nix 包管理器
nix-manager-install:
    /usr/bin/sk-nix-install install

# Uninstall the nix package manager / 卸载 nix 包管理器
nix-manager-uninstall:
    /usr/bin/sk-nix-install uninstall

# Nix search / Nix 搜索
nix-search name:
    nix-env -qaP --description --attr-path --show-trace {{name}} | cat


# Nix uptate / Nix 更新
nix-update:
    nix-channel --update

# Nix install package / Nix 安装软件包
nix-install name:
    nix-env -i {{name}}

# Nix uninstall package / Nix 卸载软件包
nix-uninstall name:
    nix-env -e {{name}}

# Nix list installed packages / Nix 列出已安装的软件包
nix-list-installed:
    nix-env -q --out-path --description | cat

# Nix 释放软件包
nix-gc:
    nix-collect-garbage -d