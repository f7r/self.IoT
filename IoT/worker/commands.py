# =============================================================================
# Author: falseuser
# File Name: commands.py
# Created Time: 2018-09-15 17:21:12
# Last modified: 2018-10-25 17:35:32
# Description:
# =============================================================================
from DataSource.system import (
    get_system_time,
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_os_platform,
)


CMD_FUNC_MAP = {
    "get_system_time": get_system_time,
    "get_cpu_usage": get_cpu_usage,
    "get_memory_usage": get_memory_usage,
    "get_disk_usage": get_disk_usage,
    "get_os_platform": get_os_platform,
}
