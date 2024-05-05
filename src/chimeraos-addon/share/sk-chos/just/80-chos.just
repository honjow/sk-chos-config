# vim: set ft=make :

# make swapfile / 重新生成 swapfile
mkswapfile:
    sudo /usr/bin/sk-mkswapfile

# fix boot entry / 修复启动项
boot-entry-fix:
    sudo /usr/bin/sk-chos-boot-fix