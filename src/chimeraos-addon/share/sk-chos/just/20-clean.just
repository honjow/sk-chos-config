# vim: set ft=make :


# etc 清理复位
[group("system")]
clean-etc:
    #!/bin/bash
    if [ -f /usr/share/sk-chos-tool/scripts/etc_repair.sh ]; then
        sudo /usr/share/sk-chos-tool/scripts/etc_repair.sh
    else
        echo "etc_repair.sh not found"
    fi

# etc 清理复位(完全)
[group("system")]
clean-etc-full:
    #!/bin/bash
    if [ -f /usr/share/sk-chos-tool/scripts/etc_repair.sh ]; then
        sudo /usr/share/sk-chos-tool/scripts/etc_repair.sh full
    else
        echo "etc_repair.sh not found"
    fi