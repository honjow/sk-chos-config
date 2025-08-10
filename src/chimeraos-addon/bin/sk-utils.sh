# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# 文字格式
BOLD='\033[1m'
UNDERLINE='\033[4m'
ITALIC='\033[3m'
STRIKETHROUGH='\033[9m'
BLINK='\033[5m'
REVERSE='\033[7m'
INVERT='\033[7m'
NORMAL='\033[0m'

# 获取当前时间戳
get_timestamp() {
    date '+%H:%M:%S'
}

# 日志函数
log_info() {
    echo -e "${GRAY}[$(get_timestamp)]${NC} ${BLUE}ℹ️ $1${NC}" >&2
}

log_success() {
    echo -e "${GRAY}[$(get_timestamp)]${NC} ${GREEN}✅ $1${NC}" >&2
}

log_warning() {
    echo -e "${GRAY}[$(get_timestamp)]${NC} ${YELLOW}⚠️ $1${NC}" >&2
}

log_error() {
    echo -e "${GRAY}[$(get_timestamp)]${NC} ${RED}❌ $1${NC}" >&2
}

log_verbose() {
    echo -e "${GRAY}[$(get_timestamp)]${NC} $1" >&2
}

# 如果直接运行此脚本（非被source）
# if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
#     main "$@"
# fi