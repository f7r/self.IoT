# =============================================================================
# Author: falseuser
# File Name: __init__.py
# Created Time: 2018-10-25 17:05:25
# Last modified: 2018-11-02 22:53:55
# Description:
# =============================================================================
import psutil
import platform
import datetime
import socket
import struct
import fcntl
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
    return datetime.datetime.now().strftime(fmt)


def get_ip():
    ifname = "eth0"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', bytes(ifname[:15], 'utf-8')),
        )[20:24]
    )
