#!/usr/bin/python3
# coding=utf-8

import time
import spidev  # SPI
import smbus   # I2C
import RPi.GPIO as GPIO


# Hardware setting
OLED_RST_PIN = 12
OLED_DC_PIN = 5
OLED_CS_PIN = 6

COM_PROTO = 1  # Communication protocol, SPI: 1, I2C: 2

# Define the full screen height length of the display
OLED_X_MAXPIXEL = 128  # OLED width maximum memory
OLED_Y_MAXPIXEL = 128  # OLED height maximum memory
OLED_X = 0
OLED_Y = 0

OLED_WIDTH = (OLED_X_MAXPIXEL - 2 * OLED_X)  # OLED width
OLED_HEIGHT = OLED_Y_MAXPIXEL                # OLED height

# buffer
BUFSIZ = int(OLED_WIDTH * OLED_HEIGHT / 2)
Buffer = [0 for i in range(BUFSIZ)]

# scanning method
L2R_U2D = 1
L2R_D2U = 2
R2L_U2D = 3
R2L_D2U = 4
U2D_L2R = 5
U2D_R2L = 6
D2U_L2R = 7
D2U_R2L = 8
SCAN_CODE = L2R_U2D


# Drive layer
class GPIOperation(object):

    def __init__(self):
        if COM_PROTO not in (1, 2):
            raise ValueError("Unsupported protocol.")
        self._gpio_init()
        self._set_proto()

    def _set_proto(self):
        if COM_PROTO == 1:  # Initialize SPI
            self.SPI = spidev.SpiDev(0, 0)
            self.SPI.max_speed_hz = 9000000
            self.SPI.mode = 0b00
        else:  # Initialize I2C
            GPIO.output(OLED_DC_PIN, GPIO.HIGH)
            self.I2C = smbus.SMBus(1)
            self.I2C_CMD = 0x00
            self.I2C_RAM = 0x40
            self.I2C_ADDR = 0x3d

    def _gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(OLED_RST_PIN, GPIO.OUT)
        GPIO.setup(OLED_DC_PIN, GPIO.OUT)
        GPIO.setup(OLED_CS_PIN, GPIO.OUT)

    def send_data(self, data):
        if COM_PROTO == 1:
            GPIO.output(OLED_DC_PIN, GPIO.HIGH)
            GPIO.output(OLED_CS_PIN, GPIO.LOW)
            data_len = len(data)
            if data_len > 4096:
                div, mod = divmod(data_len, 4096)
                for d in range(div):
                    start = d * 4096
                    end = start + 4096
                    self.SPI.writebytes(data[start:end])
                if mod > 0:
                    self.SPI.writebytes(data[end:])
            else:
                self.SPI.writebytes(data)
            GPIO.output(OLED_CS_PIN, GPIO.HIGH)
        else:
            self.I2C.write_byte_data(self.I2C_ADDR, self.I2C_RAM, data)

    def send_cmd(self, cmd):
        if COM_PROTO == 1:
            GPIO.output(OLED_DC_PIN, GPIO.LOW)
            GPIO.output(OLED_CS_PIN, GPIO.LOW)
            self.SPI.writebytes(cmd)
            GPIO.output(OLED_CS_PIN, GPIO.HIGH)
        else:
            self.I2C.write_byte_data(self.I2C_ADDR, self.I2C_CMD, cmd)

    def cleanup(self):
        GPIO.cleanup(OLED_RST_PIN)
        GPIO.cleanup(OLED_DC_PIN)
        GPIO.cleanup(OLED_CS_PIN)


class OLEDDriver(object):
    def __init__(self):
        self.scan_code = SCAN_CODE
        self.com_proto = COM_PROTO
        self.io = GPIOperation()

        self.reset()
        self.init_reg()
        self.set_scan_type()
        # self.delay_ms(200)
        self.write_reg(0xaf)

    def delay_ms(self, ms):
        time.sleep(ms/1000.0)

    """ Hardware reset """
    def reset(self):
        GPIO.output(OLED_RST_PIN, GPIO.HIGH)
        # self.delay_ms(100)
        GPIO.output(OLED_RST_PIN, GPIO.LOW)
        # self.delay_ms(100)
        GPIO.output(OLED_RST_PIN, GPIO.HIGH)
        # self.delay_ms(100)

    def close(self):
        self.io.cleanup()

    def write_reg(self, reg):
        """ Write register address and data """
        if self.com_proto == 1:
            self.io.send_cmd([reg])
        else:
            self.io.send_cmd(reg)

    def write_reg_list(self, reg_list):
        if self.com_proto == 1:
            self.io.send_cmd(reg_list)
        else:
            raise ValueError("Protocol does not support list.")

    def write_data(self, data):
        if self.com_proto == 1:
            self.io.send_data([data])
        else:
            self.io.send_data(data)

    def write_data_list(self, data_list):
        if self.com_proto == 1:
            self.io.send_data(data_list)
        else:
            raise ValueError("Protocol does not support list.")

    def init_reg(self):
        """ Common register initialization """
        reg_list = [
            0xae, 0x15, 0x00, 0x7f, 0x75, 0x00, 0x7f, 0x81, 0x80,
            0xa0, 0x51, 0xa1, 0x00, 0xa2, 0x00, 0xa4, 0xa8, 0x7f,
            0xb1, 0xf1, 0xb3, 0x00, 0xab, 0x01, 0xb6, 0x0f, 0xbe,
            0x0f, 0xbc, 0x08, 0xd5, 0x62, 0xfd, 0x12,
        ]
        self.write_reg_list(reg_list)

    def set_scan_type(self):
        """ Set the display scan and color transfer method """
        if self.scan_code == L2R_U2D:
            self.write_reg(0xa0)
            self.write_reg(0x51)
        elif self.scan_code == L2R_D2U:
            self.write_reg(0xa0)
            self.write_reg(0x41)
        elif self.scan_code == R2L_U2D:
            self.write_reg(0xa0)
            self.write_reg(0x52)
        elif self.scan_code == R2L_D2U:
            self.write_reg(0xa0)
            self.write_reg(0x42)
        else:
            raise ValueError("Unsupported Scan code.")

        if self.scan_code in (L2R_U2D, L2R_D2U, R2L_U2D, R2L_D2U):
            self.dis_column = OLED_WIDTH
            self.dis_line = OLED_HEIGHT
            self.X_offset = OLED_X
            self.Y_offset = OLED_Y
        else:
            self.dis_column = OLED_HEIGHT
            self.dis_line = OLED_WIDTH
            self.X_offset = OLED_Y
            self.Y_offset = OLED_X

    def set_window(self, x_start, y_start, x_end, y_end):
        """ Set the start position and size of the display area.
        parameters:
            x_start:   X direction start coordinate
            y_start: Y direction start coordinate
            x_end:   X direction end coordinate
            y_end: Y direction end coordinate
        """
        if x_start > self.dis_column or \
                x_end > self.dis_column or \
                y_start > self.dis_line or \
                y_end > self.dis_line:
            raise ValueError("Window setting is Out of display range.")

        reg_list = [
            0x15, x_start, x_end - 1,
            0x75, y_start, y_end - 1,
        ]
        self.write_reg_list(reg_list)

    def set_cursor(self, x_point, y_point):
        """ Set the display point
        parameter:
            x_point: X direction coordinate
            y_point: Y direction coordinate
        """
        if x_point > self.dis_column or \
                y_point > self.dis_line:
            raise ValueError("Cursor setting is Out of display range.")

        reg_list = [
            0x15, x_point, x_point,
            0x75, y_point, x_point,
        ]
        self.write_reg_list(reg_list)

    def clear(self):
        """ Clear screen """
        length = int(self.dis_line * self.dis_column / 2)
        data_list = [0x00 for i in range(length)]
        self.write_data_list(data_list)

    def show_image(self, image, x_start, y_start):
        if image is None:
            return
        self.set_window(x_start, y_start, self.dis_column, self.dis_line)
        pixels = image.load()

        x_fill = self.dis_column - image.width - x_start * 2
        pixel_color_list = []
        for l in range(0, image.height):
            for c in range(0, int(image.width / 2)):
                left_color = ((pixels[2 * c, l] & 0x0f) << 4)
                right_color = ((pixels[2 * c + 1, l] & 0x0f))
                pixel_color = left_color | right_color
                pixel_color_list.append(pixel_color)
            if x_fill >= 0:
                add_list = [0x00 for i in range(int(x_fill / 2))]
                pixel_color_list.extend(add_list)
            else:
                list_length = len(pixel_color_list)
                pop_length = int(- x_fill / 2)
                end = list_length - pop_length
                pixel_color_list = pixel_color_list[:end]

        self.write_data_list(pixel_color_list)
