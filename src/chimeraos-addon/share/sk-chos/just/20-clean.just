# vim: set ft=make :


# etc 清理复位
clean-etc:
    #!/bin/bash
    if [ -f /usr/share/sk-chos-tool/scripts/etc_repair.sh ]; then
        sudo /usr/share/sk-chos-tool/scripts/etc_repair.sh
    else
        echo "etc-repair.sh not found"
    fi

# etc 清理复位(完全)
clean-etc-full:
    #!/bin/bash
    if [ -f /usr/share/sk-chos-tool/scripts/etc_repair_full.sh ]; then
        sudo /usr/share/sk-chos-tool/scripts/etc_repair.sh full
    else
        echo "etc-repair.sh not found"
    fi