# =============================================================================
# Author: falseuser
# Created Time: 2018-11-13 16:29:39
# Last modified: 2018-11-14 17:15:06
# Description: lgsjs1b.py LGSJS1B Laser dust sensor.
# =============================================================================
from drivers import LGSJS1B


driver = LGSJS1B.DustSensor()


def get_pm_1():
    return driver.get_pm_1_2()


def get_pm_2_5():
    return driver.get_pm_2_5_2()


def get_pm_10():
    return driver.get_pm_10_2()


if __name__ == "__main__":
    print("PM1: ", get_pm_1())
    print("PM2: ", get_pm_2_5())
    print("PM3: ", get_pm_10())
