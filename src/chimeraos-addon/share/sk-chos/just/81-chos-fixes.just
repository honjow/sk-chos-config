# vim: set ft=make :
# from https://github.com/ublue-os/bazzite/blob/main/system_files/desktop/shared/usr/share/ublue-os/just/81-bazzite-fixes.just

# Fix the default Steam config to improve download speeds / 修复默认的 Steam 配置以提高下载速度
fix-steam-download-speed:
    mkdir -p $HOME/.local/share/Steam
    rm -f $HOME/.local/share/Steam/steam_dev.cfg
    bash -c 'printf "@nClientDownloadEnableHTTP2PlatformLinux 0\n@fDownloadRateImprovementToAddAnotherConnection 1.0\n" > $HOME/.local/share/Steam/steam_dev.cfg'

# Patch GMod's 64-bit beta to work properly on Linux (https://github.com/solsticegamestudios/GModCEFCodecFix)
fix-gmod:
    #!/usr/bin/bash
    mkdir -p /tmp/patch-gmod
    wget \
      $(curl -s https://api.github.com/repos/solsticegamestudios/GModCEFCodecFix/releases/latest | \
      jq -r ".assets[] | select(.name | test(\"GModCEFCodecFix-Linux\")) | .browser_download_url") \
      -P /tmp/patch-gmod
    chmod +x /tmp/patch-gmod/GModCEFCodecFix-Linux
    /tmp/patch-gmod/GModCEFCodecFix-Linux
    rm -rf /tmp/patch-gmod
