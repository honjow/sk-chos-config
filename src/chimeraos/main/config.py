import logging
import utils

LOG_LOCATION = "/tmp/sk-chos-tool.log"
logging.basicConfig(
    level = logging.INFO,
    filename = LOG_LOCATION,
    format="[%(asctime)s | %(filename)s:%(lineno)s:%(funcName)s] %(levelname)s: %(message)s",
    filemode = 'w',
    force = True)

SK_TOOL_PATH = "/usr/share/sk-chos-tool"

PRODUCT_NAME = utils.get_product_name()