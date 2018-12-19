# =============================================================================
# Author: falseuser
# File Name: __init__.py
# Created Time: 2018-11-01 17:59:49
# Last modified: 2018-11-15 11:30:55
# Description:
# =============================================================================
from .bme280 import get_pressure, get_temperature, get_humidity
from .ccs811 import get_eco2, get_tvoc
from .flame import get_fire
from .pir import get_approaching
from .lgsjs1b import get_pm_1, get_pm_2_5, get_pm_10


__all__ = [
    "get_pressure", "get_temperature", "get_humidity",
    "get_eco2", "get_tvoc", "get_fire", "get_approaching",
    "get_pm_1", "get_pm_2_5", "get_pm_10",
    "get_all_sensors",
    ]


def get_all_sensors():
    sensors = ["bme280", "ccs811", "flame", "pir", "lgsjs1b"]
    return sensors
