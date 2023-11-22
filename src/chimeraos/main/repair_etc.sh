#/bin/bash

[ "$UID" -eq 0 ] || exec sudo "$0" "$@"

# root check
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

TEMP_DIR=$(mktemp -d)
sudo touch $TEMP_DIR/repaired

TARGET_DIR=/frzr_root/etc


# --dry-run

rsync -av --delete $TEMP_DIR/ $TARGET_DIR/ \
--exclude=ssh \
--exclude=fstab \
--exclude=hostname \
--exclude=hosts \
--exclude=systemd/system/plugin_loader.service \
--exclude=systemd/system/multi-user.target.wants/plugin_loader.service \
--exclude=systemd/sleep.conf.d/sleep.conf \

chmod 755 $TARGET_DIR