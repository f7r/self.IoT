#!/usr/bin/python3
"""
Raspberry Pi BME280 Driver.
"""
import time
import smbus
import RPi.GPIO as GPIO


# Oversampling modes
X1 = 1
X2 = 2
X4 = 3
X8 = 4
X16 = 5

SENSOR_ADDR = 0x77
COM_PROTO = 2


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

    def send_data(self, data):
        raise NotImplementedError

    def get_word_data(self, register):
        if COM_PROTO == 1:
            raise NotImplementedError
        else:
            return self.I2C.read_word_data(self.I2C_ADDR, register)

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

    """
    The BME280 output consists of the ADC output values. However, each sensing
    element behaves differently. Therefore, the actual pressure and temperature
    must be calculated using a set of calibration parameters.

    The calibration parameters are subsequently used to with some compensation
    formula to perform temperature readout in degC, humidity in % and pressure
    in hPA.
    """
    def load_calibration_params(self):
        def unsigned_short(register):
            return self.get_word_data(register) & 0xffff

        def signed_short(register):
            word = unsigned_short(register)
            return word if word < 0x8000 else word - 0x10000

        def unsigned_byte(register):
            return self.get_byte_data(register) & 0xff

        def signed_byte(register):
            byte = unsigned_byte(register) & 0xff
            return byte if byte < 0x80 else byte - 0x100

        comp_params = Params()

        # Temperature trimming params
        comp_params.dig_T1 = unsigned_short(0x88)
        comp_params.dig_T2 = signed_short(0x8A)
        comp_params.dig_T3 = signed_short(0x8C)

        # Pressure trimming params
        comp_params.dig_P1 = unsigned_short(0x8E)
        comp_params.dig_P2 = signed_short(0x90)
        comp_params.dig_P3 = signed_short(0x92)
        comp_params.dig_P4 = signed_short(0x94)
        comp_params.dig_P5 = signed_short(0x96)
        comp_params.dig_P6 = signed_short(0x98)
        comp_params.dig_P7 = signed_short(0x9A)
        comp_params.dig_P8 = signed_short(0x9C)
        comp_params.dig_P9 = signed_short(0x9E)

        # Humidity trimming params
        comp_params.dig_H1 = unsigned_byte(0xA1)
        comp_params.dig_H2 = signed_short(0xE1)
        comp_params.dig_H3 = signed_byte(0xE3)

        e4 = signed_byte(0xE4)
        e5 = signed_byte(0xE5)
        e6 = signed_byte(0xE6)

        comp_params.dig_H4 = e4 << 4 | e5 & 0x0F
        comp_params.dig_H5 = ((e5 >> 4) & 0x0F) | (e6 << 4)
        comp_params.dig_H6 = signed_byte(0xE7)

        return comp_params

    def cleanup(self):
        GPIO.cleanup()


class Params(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Readings(object):

    def __init__(self, pressure, temperature, humidity):
        self.pressure = pressure
        self.temperature = temperature
        self.humidity = humidity


class SensorDriver(object):

    def __init__(self):
        self.io = GPIOperation()
        self.comp_params = self.io.load_calibration_params()

    def _get_uncompensated_readings(self, block_data):
        uncompensated_pressure = (
            block_data[0] << 16 | block_data[1] << 8 | block_data[2]
        ) >> 4
        uncompensated_temperature = (
            block_data[3] << 16 | block_data[4] << 8 | block_data[5]
        ) >> 4
        uncompensated_humidity = block_data[6] << 8 | block_data[7]
        uncompensated_readings = Readings(
            uncompensated_pressure,
            uncompensated_temperature,
            uncompensated_humidity,
        )
        return uncompensated_readings

    """
    Compensation formulas translated,from Appendix A (8.1) of BME280 datasheet
    """
    def _get_compensated_readings(self, uncompensated_readings):
        compensated_pressure = self.__calc_pressure(
            uncompensated_readings.pressure,
            uncompensated_readings.temperature,
        ) / 100.0
        compensated_temperature = self.__tfine(
            uncompensated_readings.temperature,
        ) / 5120.0
        compensated_humidity = self.__calc_humidity(
            uncompensated_readings.humidity,
            uncompensated_readings.temperature,
        )
        compensated_readings = Readings(
            compensated_pressure,
            compensated_temperature,
            compensated_humidity,
        )
        return compensated_readings

    def __tfine(self, t):
        v1 = t / 16384.0
        v2 = self.comp_params.dig_T1 / 1024.0
        v3 = t / 131072.0
        v4 = self.comp_params.dig_T1 / 8192.0
        v5 = (v1 - v2) * self.comp_params.dig_T2
        v6 = ((v3 - v4) ** 2) * self.comp_params.dig_T3
        value = v5 + v6
        return value

    def __calc_humidity(self, h, t):
        v1 = self.__tfine(t) - 76800.0
        v2 = self.comp_params.dig_H4 * 64.0
        v3 = self.comp_params.dig_H5 / 16384.0
        v4 = self.comp_params.dig_H2 / 65536.0
        v5 = self.comp_params.dig_H6 / 67108864.0
        v6 = self.comp_params.dig_H3 / 67108864.0
        v7 = (h - (v2 + v3 * v1)) * (v4 * (1.0 + v5 * v1 * (1.0 + v6 * v1)))
        v8 = self.comp_params.dig_H1 / 524288.0
        v9 = v7 * (1.0 - v8 * v7)
        value = max(0.0, min(v9, 100.0))
        return value

    def __calc_pressure(self, p, t):
        v1 = self.__tfine(t) / 2.0 - 64000.0
        v2 = self.comp_params.dig_P6 / 32768.0
        v3 = v1 * v1 * v2
        v4 = v3 + v1 * self.comp_params.dig_P5 * 2.0
        v5 = v4 / 4.0 + self.comp_params.dig_P4 * 65536.0
        v6 = self.comp_params.dig_P3 / 524288.0
        v7 = (v1 * v1 * v6 + self.comp_params.dig_P2 * v1) / 524288.0
        v8 = (1.0 + v7 / 32768.0) * self.comp_params.dig_P1

        # Prevent divide by zero
        if v8 == 0:
            return 0

        v9 = 1048576.0 - p
        v10 = ((v9 - v5 / 4096.0) * 6250.0) / v8

        v11 = self.comp_params.dig_P9 * v10 * v10 / 2147483648.0
        v12 = self.comp_params.dig_P8 * v10 / 32768.0
        value = v10 + (v11 + v12 + self.comp_params.dig_P7) / 16.0

        return value

    def __calc_delay(self, t_overs, h_overs, p_overs):
        t_delay = 0.000575 + 0.0023 * (1 << t_overs)
        h_delay = 0.000575 + 0.0023 * (1 << h_overs)
        p_delay = 0.001250 + 0.0023 * (1 << p_overs)
        return t_delay + h_delay + p_delay

    def sample(self, overs=X1):
        mode = 1
        t_overs = overs
        h_overs = overs
        p_overs = overs
        self.io.send_cmd(0xF2, h_overs)
        byte_data = t_overs << 5 | p_overs << 2 | mode
        self.io.send_cmd(0xF4, byte_data)
        delay = self.__calc_delay(t_overs, h_overs, p_overs)
        time.sleep(delay)

        block_data = self.io.get_block_data(0xF7, 8)
        uncomp_readings = self._get_uncompensated_readings(block_data)
        comp_readings = self._get_compensated_readings(uncomp_readings)
        return comp_readings
