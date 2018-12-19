# =============================================================================
# Author: falseuser
# Created Time: 2018-12-19 10:04:19
# Last modified: 2018-12-19 12:06:57
# Description: standalone.py
# =============================================================================
import time
# from operations import system
from operations.hardware import sensors, display


def get_data():
    data = {}
    try:
        data["eco2"] = sensors.get_eco2()
    except ValueError:
        data["eco2"] = None
    try:
        data["tvoc"] = sensors.get_tvoc()
    except ValueError:
        data["tvoc"] = None
    data["temperature"] = sensors.get_temperature()
    data["humidity"] = sensors.get_humidity()
    data["pressure"] = sensors.get_pressure()
    data["pm_1"] = sensors.get_pm_1()
    data["pm_2_5"] = sensors.get_pm_2_5()
    data["pm_10"] = sensors.get_pm_10()
    return data


def show(data):
    lines = [
        "",
        "Eco2: {0}".format(data['eco2']),
        "Tvoc: {0}".format(data['tvoc']),
        "Tmp: {0:.2f} deC".format(data['temperature']),
        "Hum: {0:.2f} %".format(data['humidity']),
        "Pre: {0:.2f} hPa".format(data['pressure']),
        "PM 1: {0}".format(data['pm_1']),
        "PM 2.5 {0}".format(data['pm_2_5']),
        "PM 10 {0}".format(data['pm_10']),
        "",
    ]
    d = display.Display()
    d.show_lines(lines)


if __name__ == "__main__":
    while True:
        time.sleep(1)
        if sensors.get_approaching():
            print("开始读取数据")
            data = get_data()
            print("显示数据")
            show(data)
