# modify from https://github.com/ublue-os/config/blob/main/build/ublue-os-just/etc-profile.d/user-motd.sh
if test -d "$HOME"; then
  if test ! -e "$HOME"/.config/no-show-user-motd; then
    if test -x "/usr/libexec/chos-motd"; then
      /usr/libexec/chos-motd
    elif test -s "/etc/user-motd"; then
      cat /etc/user-motd
    fi
  fi
fi