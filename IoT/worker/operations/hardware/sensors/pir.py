# =============================================================================
# Author: falseuser
# File Name: PIR.py
# Created Time: 2018-11-01 17:49:14
# Last modified: 2018-11-13 16:21:27
# Description:
# =============================================================================
from .drivers import PIR


__all__ = ["get_approaching"]


pir = PIR.PIRDriver()


def get_approaching():
    return pir.get_approaching()
