# vim: set ft=make :

# rEFInd 安装配置
setup-refind ACTION="":
    #!/usr/bin/bash
    set -eu
    source /usr/lib/cjust/cjust.sh
    OPTION={{ ACTION }}
    if [ "$OPTION" == "help" ]; then
      echo "Usage: cjust setup-refind <option>"
      echo "  <option> 快速设置选项"
      echo "  'install' 安装并配置 rEFInd"
      echo "  'setup' 更新 rEFInd 配置"
      echo "  'uninstall' 卸载 rEFInd"
      exit 0
    elif [ "$OPTION" == "" ]; then
      echo "${bold}rEFInd Setup${normal}"
      OPTION=$(Choose \
        "安装并配置 rEFInd" \
        "更新 rEFInd 配置" \
        "卸载 rEFInd" \
        )
    fi
    if [[ "${OPTION,,}" =~ ^install ]]; then
      pkexec /usr/libexec/setup-refind install
    elif [[ "${OPTION,,}" =~ ^setup ]]; then
      pkexec /usr/libexec/setup-refind setup
    elif [[ "${OPTION,,}" =~ uninstall ]]; then
      pkexec /usr/libexec/setup-refind uninstall
    fi
