#!/usr/bin/python3
"""
Raspberry Pi PIR Driver.
"""
import time
import RPi.GPIO as GPIO


PIR_PIN = 23


class GPIOperation(object):

    def __init__(self):
        self._gpio_init()

    def _gpio_init(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIR_PIN, GPIO.IN)

    def get_high(self):
        return GPIO.input(PIR_PIN)

    def cleanup(self):
        GPIO.cleanup(PIR_PIN)


class PIRDriver(object):

    def __init__(self):
        self.io = GPIOperation()

    def get_approaching(self):
        if self.io.get_high():
            return True
        else:
            time.sleep(3)
            return self.io.get_high()
