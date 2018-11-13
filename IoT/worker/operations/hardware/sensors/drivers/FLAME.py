# =============================================================================
# Author: falseuser
# Created Time: 2018-11-12 23:13:38
# Last modified: 2018-11-13 16:05:57
# Description: FLAME.py Raspberry Pi flame sensor Driver.
# =============================================================================
import RPi.GPIO as GPIO


FLAME_PIN = 23


class GPIOperation(object):

    def __init__(self):
        self._gpio_init()

    def _gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(FLAME_PIN, GPIO.IN)

    def get_high(self):
        return GPIO.input(FLAME_PIN)

    def cleanup(self):
        GPIO.cleanup(FLAME_PIN)


class FLAMEDriver(object):

    def __init__(self):
        self.io = GPIOperation()

    def get_fire(self):
        return not self.io.get_high()
