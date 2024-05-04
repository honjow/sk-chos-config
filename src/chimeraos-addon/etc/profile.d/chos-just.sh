# Add uBlue's justfiles to users with home directories which lack a justfile.
# from https://github.com/ublue-os/config/blob/main/build/ublue-os-just/etc-profile.d/ublue-os-just.sh

if [ ! -z "$HOME" ] && [ -d "$HOME" ] && [ ! -f "${HOME}/.justfile" ]; then
  cat > "${HOME}/.justfile" << EOF
import "/usr/share/sk-chos/justfile"
EOF
fi

if [ -f "${HOME}/.justfile" ]; then
  if ! grep -Fxq 'import "/usr/share/sk-chos/justfile"' "${HOME}/.justfile"; then
    # Remove any lines we may have added previously.
    sed -i '/!include \/usr\/share\/sk-chos\/just\/.*.just/d' "${HOME}/.justfile"
    sed -i '/!include \/usr\/share\/sk-chos\/justfile/d' "${HOME}/.justfile"

    # Point to the new main justfile, place it as the first line
    echo '# You can add your own commands here! ' | tee -a "${HOME}/.justfile"
    echo 'import "/usr/share/sk-chos/justfile"' | tee -a "${HOME}/.justfile"
  fi
fi