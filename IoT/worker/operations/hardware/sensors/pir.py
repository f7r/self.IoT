# =============================================================================
# Author: falseuser
# File Name: PIR.py
# Created Time: 2018-11-01 17:49:14
# Last modified: 2018-11-02 22:24:59
# Description:
# =============================================================================
from .drivers import PIR


pir = PIR.PIRDriver()


def get_approaching():
    return pir.get_approaching()
