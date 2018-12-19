# =============================================================================
# Author: falseuser
# File Name: oled.py
# Created Time: 2018-11-02 16:30:00
# Last modified: 2018-12-19 12:07:04
# Description:
# =============================================================================
import os
import time
import threading
from PIL import Image, ImageDraw, ImageFont
from .drivers import Driver


class Display(object):

    def __init__(self):
        self._load_font()
        self.stoped = False
        self.driver = Driver.OLEDDriver()

    def _load_font(self):
        _path = os.path.dirname(os.path.realpath(__file__))
        self.font_file = "{0}/consola_ascii.ttf".format(_path)
        self.font_14 = ImageFont.truetype(self.font_file, size=14)

    def on(self):
        t = threading.Thread(target=self.show_all)
        t.start()

    def show_lines(self, lines):
        image = self.get_image(lines)
        self.scroll_display(image)

    def scroll_display(self, image):
        self.driver.clear()
        if image.height > 128:
            for h in range(128, image.height):
                # self.driver.clear()
                box = (0, h - 128, 128, h)
                dis_image = image.crop(box)
                self.driver.show_image(dis_image, 0, 0)
                time.sleep(0.2)
        else:
            self.driver.show_image(image, 0, 0)
        self.driver.clear()

    def get_image(self, lines):
        height = len(lines) * 16
        width = 128
        image = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(image)
        text_lines = ""
        for line in lines:
            text_lines = text_lines + line + "\n"
        draw.multiline_text(
            (0, 0),
            text=text_lines,
            font=self.font_14,
            fill="White",
        )
        return image
