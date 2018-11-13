# =============================================================================
# Author: falseuser
# Created Time: 2018-11-13 16:29:39
# Last modified: 2018-11-13 16:43:15
# Description: lgsjs1b.py LGSJS1B Laser dust sensor.
# =============================================================================
from .drivers import LGSJS1B


driver = LGSJS1B.DustSensor()


def get_pm_1():
    pass


def get_pm_2_5():
    pass


def get_pm_10():
    pass
