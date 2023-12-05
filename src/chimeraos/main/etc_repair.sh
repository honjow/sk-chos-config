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


if [[ $1 == "full" ]];then
  rsync -av --delete $TEMP_DIR/ $TARGET_DIR/ \
      --exclude=fstab \
      --exclude=localtime \
      --exclude=locale.conf \
      --exclude=passwd \
      --exclude=systemd/system/plugin_loader.service \
      --exclude=systemd/system/multi-user.target.wants/plugin_loader.service

else
  rsync -av --delete $TEMP_DIR/ $TARGET_DIR/ \
      --exclude=ssh \
      --exclude=fstab \
      --exclude=hostname \
      --exclude=pipewire \
      --exclude=NetworkManager \
      --exclude=localtime \
      --exclude=locale.conf \
      --exclude=passwd \
      --exclude=systemd/system/plugin_loader.service \
      --exclude=systemd/system/multi-user.target.wants/plugin_loader.service \
      --exclude=systemd/sleep.conf.d/sleep.conf

fi

# --dry-run

rm $TARGET_DIR/repaired

chmod 755 $TARGET_DIR