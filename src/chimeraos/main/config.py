import logging
import os

SK_TOOL_PATH = "/usr/share/sk-chos-tool"

PANED_RIGHT_MARGIN_START = 20
PANED_RIGHT_MARGIN_END = 20
PANED_RIGHT_MARGIN_TOP = 8
PANED_RIGHT_MARGIN_BOTTOM = 20

LOG_LOCATION = "/tmp/sk-chos-tool.log"
logging.basicConfig(
    level = logging.INFO,
    format="[%(asctime)s | %(filename)s:%(lineno)s:%(funcName)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_LOCATION, mode="a", encoding="utf-8")
    ],
    force = True)

def get_product_name():
    product_name = ""
    try:
        with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
            product_name = f.readline().strip()
    except Exception as e:
        logging.error(f"读取设备名称失败: {e}")
    logging.info(f"设备名称: {product_name}")
    return product_name

PRODUCT_NAME = get_product_name()

USER = os.getenv("USER")

HHD_SUPPORT_PRODUCT_NAME = [
    "83E1",
    "ROG Ally RC71L_RC71L",
    "ROG Ally RC71L",
    "G1618-04",
    "G1617-01",
    "AIR Plus",
    "AYANEO 2",
    "AYANEO 2S",
    "GEEK",
    "GEEK 1S",
]