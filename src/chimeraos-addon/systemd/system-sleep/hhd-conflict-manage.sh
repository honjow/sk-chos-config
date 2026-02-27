#!/bin/bash

# After resume, udev may reload conflict modules when USB devices re-enumerate.
# Schedule a delayed re-unload to catch modules loaded after USB re-enumeration.

case "$1" in
    post)
        systemctl is-active --quiet hhd-conflict-manage.service 2>/dev/null || exit 0
        systemd-run --no-block --on-active=3 --collect \
            --unit=hhd-conflict-manage-post-resume \
            /usr/bin/hhd-conflict-manage _post-resume || true
        ;;
esac
