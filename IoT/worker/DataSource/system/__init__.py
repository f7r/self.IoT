# =============================================================================
# Author: falseuser
# File Name: __init__.py
# Created Time: 2018-10-25 17:05:25
# Last modified: 2018-10-25 17:32:49
# Description:
# =============================================================================
import psutil
import platform
import datetime
import json


def get_cpu_usage():
    return psutil.cpu_percent()


def get_memory_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage("/").percent


def get_os_platform():
    kernel_version = platform.release()
    python_version = platform.python_version()
    distribution = platform.linux_distribution()
    os_platform = {
        "OS distribution": distribution[0],
        "Distribution version": distribution[1],
        "Codename": distribution[2],
        "Development language": "Python",
        "language version": python_version,
        "Kernel version": kernel_version,
    }
    return json.dumps(os_platform)


def get_system_time():
    fmt = "%Y-%m-%d %H:%M:%S"
    system_time = datetime.datetime.now().strftime(fmt)
    return system_time
