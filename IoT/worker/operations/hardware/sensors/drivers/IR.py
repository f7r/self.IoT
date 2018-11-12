#!/usr/bin/python3
"""
Raspberry Pi Infrared remote control Driver.
"""
import subprocess


class IRDriver(object):

    def __init__(self):
        self.conf_dir = "ir.conf"

    def send(self, key)
