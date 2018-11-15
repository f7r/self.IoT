# =============================================================================
# Author: falseuser
# File Name: commands.py
# Created Time: 2018-09-15 17:21:12
# Last modified: 2018-11-15 12:12:03
# Description:
# =============================================================================
from operations import system
from operations.hardware import sensors, head


CMD_FUNC_MAP = {
    "get_system_time": system.get_system_time,
    "get_cpu_usage": system.get_cpu_usage,
    "get_memory_usage": system.get_memory_usage,
    "get_disk_usage": system.get_disk_usage,
    "get_os_platform": system.get_os_platform,
    "get_all_sensors": sensors.get_all_sensors,
    "get_approaching": sensors.get_approaching,
    "get_eco2": sensors.get_eco2,
    "get_tvoc": sensors.get_tvoc,
    "get_temperature": sensors.get_temperature,
    "get_humidity": sensors.get_humidity,
    "get_pressure": sensors.get_pressure,
    "get_pm_1": sensors.get_pm_1,
    "get_pm_2_5": sensors.get_pm_2_5,
    "get_pm_10": sensors.get_pm_10,
    "head_start_turn": head.servo.start_turn,
    "head_end_turn": head.servo.end_turn,
    "head_turn_up": head.servo.turn_up,
    "head_turn_down": head.servo.turn_down,
    "head_turn_left": head.servo.turn_left,
    "head_turn_right": head.servo.turn_right,
}
