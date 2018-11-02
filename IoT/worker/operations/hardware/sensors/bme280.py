#!/usr/bin/python3
# =============================================================================
# Author: falseuser
# File Name: bme280.py
# Created Time: 2018-10-29 22:40:03
# Last modified: 2018-11-02 22:12:32
# Description:
# =============================================================================
from .drivers import BME280


driver = BME280.SensorDriver()


def get_pressure(self):
    data = driver.sample()
    return data.pressure


def get_temperature(self):
    data = driver.sample()
    return data.temperature


def get_humidity(self):
    data = driver.sample()
    return data.humidity
