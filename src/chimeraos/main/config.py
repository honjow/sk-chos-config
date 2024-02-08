import logging
import os

SK_TOOL_PATH = "/usr/share/sk-chos-tool"
SK_TOOL_SCRIPTS_PATH = f"{SK_TOOL_PATH}/scripts"

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

def get_vendor_name():
    vendor_name = ""
    try:
        with open("/sys/devices/virtual/dmi/id/board_vendor", "r") as f:
            vendor_name = f.readline().strip()
    except Exception as e:
        logging.error(f"读取设备厂商名称失败: {e}")
    logging.info(f"设备厂商名称: {vendor_name}")
    return vendor_name

PRODUCT_NAME = get_product_name()

VENDOR_NAME = get_vendor_name()

USER = os.getenv("USER")

hhd_support_product = [
    "83E1",
    "ROG Ally RC71L_RC71L",
    "ROG Ally RC71L",
    "G1618-04",
    "G1617-01",
    "G1619-04",
    "G1619-05",
    "AYANEO 2",
    "AYANEO 2S",
    "GEEK",
    "GEEK 1S",
    "AIR",
    "AIR Pro",
    "AIR Plus",
    "AIR 1S",
    "AIR 1S Limited",
    "AOKZOE A1 AR07",
    "AOKZOE A1 Pro",
    "ONEXPLAYER Mini Pro",
    "Loki Max",
]

hhd_support_vendor = [
    "AYANEO",
    "GPD",
]

def is_hhd_support():
    return PRODUCT_NAME in hhd_support_product or VENDOR_NAME in hhd_support_vendor

IS_HHD_SUPPORT = is_hhd_support()