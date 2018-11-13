# =============================================================================
# Author: falseuser
# Created Time: 2018-11-12 23:11:01
# Last modified: 2018-11-13 14:34:02
# Description: PCA9685.py Raspi PCA9685 16-Channel PWM Servo Driver
# =============================================================================
import time
import smbus
import RPi.GPIO as GPIO


OE_PIN = 22
CHIP_ADDR = 0x40
COM_PROTO = 2


class GPIOperation(object):

    def __init__(self):
        if COM_PROTO not in (1, 2):
            raise ValueError("Unsupported protocol.")
        self._gpio_init()
        self._set_proto()

    def _gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(OE_PIN, GPIO.OUT)
        GPIO.output(OE_PIN, GPIO.LOW)

    def _set_proto(self):
        if COM_PROTO == 1:
            pass
        else:
            self.I2C = smbus.SMBus(1)
            self.I2C_ADDR = CHIP_ADDR

    def send_cmd(self, register, cmd):
        if COM_PROTO == 1:
            raise NotImplementedError
        else:
            self.I2C.write_byte_data(self.I2C_ADDR, register, cmd)

    def get_byte_data(self, register):
        if COM_PROTO == 1:
            raise NotImplementedError
        else:
            return self.I2C.read_byte_data(self.I2C_ADDR, register)

    def sleep(self):
        GPIO.output(OE_PIN, GPIO.HIGH)

    def wake(self):
        GPIO.output(OE_PIN, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup(OE_PIN)


class CHIPDriver(object):

    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALLLED_ON_L = 0xFA
    __ALLLED_ON_H = 0xFB
    __ALLLED_OFF_L = 0xFC
    __ALLLED_OFF_H = 0xFD

    def __init__(self, address=0x40, debug=False):
        self.io = GPIOperation()
        self.io.send_cmd(self.__MODE1, 0x00)

    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0  # 25MHz
        v1 = prescaleval / 4096.0  # 12-bit
        v2 = v1 / float(freq)
        v3 = v2 - 0.5
        prescale = int(v3)

        oldmode = self.io.get_byte_data(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        self.io.send_cmd(self.__MODE1, newmode)
        self.io.send_cmd(self.__PRESCALE, prescale)
        self.io.send_cmd(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.io.send_cmd(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        self.io.send_cmd(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.io.send_cmd(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.io.send_cmd(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.io.send_cmd(self.__LED0_OFF_H + 4 * channel, off >> 8)

    def setServoPulse(self, channel, pulse):
        "Sets the Servo Pulse,The PWM frequency must be 50HZ"
        pulse = pulse * 4096 / 20000  # 50HZ,the period is 20000us
        self.setPWM(channel, 0, int(pulse))

    def sleep(self):
        self.io.sleep()

    def wake(self):
        self.io.wake()
