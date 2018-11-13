# =============================================================================
# Author: falseuser
# File Name: __init__.py
# Created Time: 2018-11-01 17:59:49
# Last modified: 2018-11-13 16:26:22
# Description:
# =============================================================================
from .bme280 import get_pressure, get_temperature, get_humidity
from .ccs811 import get_eco2, get_tvoc
from .flame import get_fire
from .pir import get_approaching


__all__ = [
    "get_pressure", "get_temperature", "get_humidity",
    "get_eco2", "get_tvoc", "get_fire", "get_approaching",
    "get_all_sensors",
    ]


def get_all_sensors():
    sensors = ["bme280", "ccs811", "flame", "pir"]
    return sensors
