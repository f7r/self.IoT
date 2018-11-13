# =============================================================================
# Author: falseuser
# Created Time: 2018-11-13 16:07:23
# Last modified: 2018-11-13 16:21:07
# Description: flame.py
# =============================================================================
from .drivers import FLAME


__all__ = ["get_fire"]


driver = FLAME.FLAMEDriver()


def get_fire():
    return driver.get_fire()
