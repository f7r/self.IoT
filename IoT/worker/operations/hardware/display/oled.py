# =============================================================================
# Author: falseuser
# File Name: oled.py
# Created Time: 2018-11-02 16:30:00
# Last modified: 2018-11-02 22:55:14
# Description:
# =============================================================================
import time
import datetime
import threading
from PIL import Image, ImageDraw, ImageFont
from IoT.worker.operations import system
from .drivers import Driver


class Display(object):

    def __init__(self):
        self._load_font()
        self.stoped = False
        self.driver = Driver.OLEDDriver()

    def _load_font(self):
        self.font_file = "consola_ascii.ttf"
        self.font_14 = ImageFont.truetype(self.font_file, size=14)

    def on(self):
        t = threading.Thread(target=self.show_all)
        t.start()

    def show_all(self):
        if not self.stoped:
            self.driver.clear()
            self._show_all()
            time.sleep(1)
        self.driver.clear()

    def _show_all(self):
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        time_string = now.strftime("%H:%M:%S")
        ip = system.get_ip()
        cpu = system.get_cpu_usage()
        mem = system.get_memory_usage()
        lines_dict = {
            0: "IP: {0}\n".format(ip),
            1: "Date: {0}\n".format(date_string),
            2: "Time: {0}\n".format(time_string),
            3: "CPU: {0}%\n".format(cpu),
            4: "Memory: {0}%\n".format(mem),
            5: "Sensors: {0}\n".format(3),
        }
        image = Image.new("L", (128, 128), 0)
        text_lines = ""
        for line in lines_dict.values():
            text_lines = text_lines + line
        draw = ImageDraw.Draw(image)
        draw.multiline_text(
            (0, 0),
            text=text_lines,
            font=self.font14,
            fill="White",
        )
        self.driver.show_image(image, 0, 0)

    def off(self):
        self.stoped = True
