# =============================================================================
# Author: falseuser
# Created Time: 2018-11-13 16:31:06
# Last modified: 2018-11-13 16:41:09
# Description: LGSJS1B.py
# =============================================================================
import time
import serial


SERIAL_DEVICE = "/dev/ttyAMA0"


class DustSensor(object):

    def __init__(self):
        self.io = serial.Serial(SERIAL_DEVICE, 9600)

    def get_raw_data(self):
        count = self.io.inWaiting()
        if count == 32:
            raw_data = self.io.read(count)
        self.io.flushInput()
        time.sleep(0.1)
        return raw_data

    def sleep(self):
        pass

    def wake(self):
        pass

    def get_pm_1(self):
        pass

    def get_pm_2_5(self):
        pass

    def get_pm_10(self):
        pass

    def close(self):
        self.io.close()
