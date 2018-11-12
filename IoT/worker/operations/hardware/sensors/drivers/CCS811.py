#!/usr/bin/python3
"""
Raspberry Pi CCS811 Driver.
"""
import time
#import Adafruit_PureIO.smbus as smbus
import smbus2 as smbus
#import smbus
import RPi.GPIO as GPIO

SENSOR_ADDR = 0x5B
COM_PROTO = 2
RST_PIN = 27
WAKE_PIN = 24


class GPIOperation(object):

    def __init__(self):
        if COM_PROTO not in (1, 2):
            raise ValueError("Unsupported protocol.")
        self._gpio_init()
        self._set_proto()

    def _gpio_init(self):
        pass

    def _set_proto(self):
        if COM_PROTO == 1:
            pass
        else:
            self.I2C = smbus.SMBus(1)
            self.I2C_ADDR = SENSOR_ADDR

    def send_cmd(self, register, cmd):
        if COM_PROTO == 1:
            raise NotImplementedError
        else:
            self.I2C.write_byte_data(self.I2C_ADDR, register, cmd)

    def send_direct(self, register):
        if COM_PROTO == 1:
            raise NotImplementedError
        else:
            self.I2C.write_byte(self.I2C_ADDR, register)

    def send_block_data(self, register, data_list):
        if COM_PROTO == 1:
            raise NotImplementedError
        else:
            self.I2C.write_i2c_block_data(self.I2C_ADDR, register, data_list)

    def get_byte_data(self, register):
        if COM_PROTO == 1:
            raise NotImplementedError
        else:
            return self.I2C.read_byte_data(self.I2C_ADDR, register)

    def get_block_data(self, register, length):
        if COM_PROTO == 1:
            raise NotImplementedError
        else:
            return self.I2C.read_i2c_block_data(
                self.I2C_ADDR, register, length)

    def cleanup(self):
        GPIO.cleanup()


class SensorDriver(object):

    def __init__(self):
        self.io = GPIOperation()
        self._sensor_init()

    def _sensor_init(self):
        self._set_mode()
        self._start_app()
        self._set_mode()
        self._start_app()
        time.sleep(0.1)

    def _set_mode(self):
        self.io = GPIOperation()
        self.io.send_cmd(0x01, 0x10)  # 00010000, 1 sec, no INT

    def _start_app(self):
        self.io.send_direct(0xF4)

    def has_error(self):
        data = self.io.get_byte_data(0xE0)
        if data != 0:
            return True
        else:
            return False

    def reset(self, hard=False):
        if hard:
            pass
        else:
            data_list = [0x11, 0xE5, 0x72, 0x8A]
            self.io.send_block_data(0xFF, data_list)

    def sample(self):
        data = self.io.get_block_data(0x02, 8)
        eCO2 = (data[0] << 8) | (data[1])
        TVOC = (data[2] << 8) | (data[3])
        error_id = data[5]
        if error_id == 0:
            return eCO2, TVOC
        else:
            return 1000000000, error_id

if __name__ == "__main__":
    driver = SensorDriver()
    for i in range(10):
        time.sleep(2)
        eCO2, TVOC = driver.sample()
        if 400 <= eCO2 < 32768 and 0 <= TVOC <= 32768:
            print(eCO2, TVOC)
        else:
            print("invalid value")
    driver.reset()
