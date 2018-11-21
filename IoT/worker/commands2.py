# =============================================================================
# Author: falseuser
# File Name: commands.py
# Created Time: 2018-09-15 17:21:12
# Last modified: 2018-11-21 17:03:53
# Description:
# =============================================================================
from operations import system


CMD_FUNC_MAP = {
    "get_system_time": system.get_system_time,
    "get_cpu_usage": system.get_cpu_usage,
    "get_memory_usage": system.get_memory_usage,
    "get_disk_usage": system.get_disk_usage,
    "get_os_platform": system.get_os_platform,
}
