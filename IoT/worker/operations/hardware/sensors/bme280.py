#!/usr/bin/python3
# =============================================================================
# Author: falseuser
# File Name: bme280.py
# Created Time: 2018-10-29 22:40:03
# Last modified: 2018-11-13 16:18:27
# Description:
# =============================================================================
from .drivers import BME280


__all__ = ["get_pressure", "get_temperature", "get_humidity"]


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
