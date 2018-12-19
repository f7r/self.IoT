# =============================================================================
# Author: falseuser
# Created Time: 2018-12-19 10:04:19
# Last modified: 2018-12-19 12:06:57
# Description: standalone.py
# =============================================================================
import time
# from operations import system
from operations.hardware import sensors
from operations.hardware.display import oled


def get_data():
    data = {}
    data["eco2"] = sensors.get_eco2()
    data["tvoc"] = sensors.get_tvoc()
    data["temperature"] = sensors.get_temperature()
    data["humidity"] = sensors.get_humidity()
    data["pressure"] = sensors.get_pressure()
    data["pm_1"] = sensors.get_pm_1()
    data["pm_2_5"] = sensors.get_pm_2_5()
    data["pm_10"] = sensors.get_pm_10()
    return data


def display(data):
    lines = [
        "Eco2: {0}".format(data['eco2']),
        "Tvoc: {0}".format(data['tvoc']),
        "Temp: {0} deC".format(data['temperature']),
        "Humi: {0} %".format(data['humidity']),
        "Pres: {0} hPa".format(data['pressure']),
        "PM 1: {0}".format(data['pm_1']),
        "PM 2.5 {0}".format(data['pm_2_5']),
        "PM 10 {0}".format(data['pm_10']),
        "",
        "",
    ]
    d = oled.Display()
    d.show_lines(lines)


if __name__ == "__main__":
    while True:
        time.sleep(1)
        if sensors.get_approaching():
            data = get_data()
            display(data)
