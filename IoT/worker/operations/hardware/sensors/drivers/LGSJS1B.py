# =============================================================================
# Author: falseuser
# Created Time: 2018-11-13 16:31:06
# Last modified: 2018-11-14 16:51:59
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

    def get_list_data(self, raw_data):
        try:
            list_data = list(raw_data)
            return list_data
        except Exception:
            raise ValueError("Illegal data.")

    def sleep(self):
        pass

    def wake(self):
        pass

    def _check_data(self, data):
        conditions = [
            len(data) == 32,
            data[0] == 0x42,
            data[1] == 0x4D,
            data[2] == 0x00,
            data[3] == 0x1C,
        ]
        return all(conditions)

    def _get_concentration(self, h8bit, l8bit):
        raw_data = self.get_raw_data()
        data = self.get_list_data(raw_data)
        if self._check_data(data):
            return data[h8bit] << 8 | data[l8bit]
        else:
            raise ValueError("Illegal data.")

    def get_pm_1_1(self):
        return self._get_concentration(4, 5)

    def get_pm_2_5_1(self):
        return self._get_concentration(6, 7)

    def get_pm_10_1(self):
        return self._get_concentration(8, 9)

    def get_pm_1_2(self):
        return self._get_concentration(10, 11)

    def get_pm_2_5_2(self):
        return self._get_concentration(12, 13)

    def get_pm_10_2(self):
        return self._get_concentration(14, 15)

    def close(self):
        self.io.close()
