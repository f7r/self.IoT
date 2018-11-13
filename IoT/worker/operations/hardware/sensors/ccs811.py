# =============================================================================
# Author: falseuser
# Created Time: 2018-11-13 15:20:17
# Last modified: 2018-11-13 16:20:32
# Description: ccs811.py
# =============================================================================
from .drivers import CCS811


__all__ = ["get_eco2", "get_tvoc"]


driver = CCS811.SensorDriver()


def get_eco2():
    "Equivalent carbon dioxide"
    data = driver.sample()
    return data.eco2


def get_tvoc():
    "Total volatile organic compound"
    data = driver.sample()
    return data.tvoc
