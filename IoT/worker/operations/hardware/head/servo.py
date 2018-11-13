# =============================================================================
# Author: falseuser
# Created Time: 2018-11-13 14:31:09
# Last modified: 2018-11-13 15:16:40
# Description: servo.py
# =============================================================================
import time
from drivers import PCA9685


LR_CHANNEL = 9  # Left-right servo
UD_CHANNEL = 8  # up-down servo


class ServoController(object):

    def __init__(self):
        self.driver = PCA9685.CHIPDriver()
        self.driver.setPWMFreq(50)  # 50Hz
        self.pulse_time_per_degree = (2500 - 500) / 180
        self.reset()

    def reset(self):
        # Reset servos angle
        lr_degree = 100
        up_degree = 80
        lr_pulse_time = 500 + self.pulse_time_per_degree * lr_degree
        ud_pulse_time = 500 + self.pulse_time_per_degree * up_degree
        self.driver.setServoPulse(LR_CHANNEL, lr_pulse_time)
        time.sleep(0.02)  # 50Hz, least sleep 20ms
        self.driver.setServoPulse(UD_CHANNEL, ud_pulse_time)
        time.sleep(0.02)
        self.current_lr_angle = lr_degree
        self.current_ud_angle = up_degree
        self.current_lr_time = lr_pulse_time
        self.current_ud_time = ud_pulse_time
        self.driver.sleep()
        self.status = "sleep"

    def _limit_angle(self):
        if self.current_lr_angle > 160:
            self.current_lr_angle = 160
            self.current_lr_time = 500 + self.pulse_time_per_degree * 160
        if self.current_lr_angle < 20:
            self.current_lr_angle = 20
            self.current_lr_time = 500 + self.pulse_time_per_degree * 20
        if self.current_ud_angle > 160:
            self.current_ud_angle = 160
            self.current_ud_time = 500 + self.pulse_time_per_degree * 160
        if self.current_ud_angle < 20:
            self.current_ud_angle = 20
            self.current_ud_time = 500 + self.pulse_time_per_degree * 20

    def turn_left(self, degree):
        if self.status == "sleep":
            return
        target_angle = self.current_lr_angle + degree
        pulse_time = self.current_lr_time + degree * self.pulse_time_per_degree
        self.driver.setServoPulse(LR_CHANNEL, pulse_time)
        time.sleep(0.02)
        self.current_lr_time = pulse_time
        self.current_lr_angle = target_angle
        self._limit_angle()

    def turn_right(self, degree):
        if self.status == "sleep":
            return
        target_angle = self.current_lr_angle - degree
        pulse_time = self.current_lr_time - degree * self.pulse_time_per_degree
        self.driver.setServoPulse(LR_CHANNEL, pulse_time)
        time.sleep(0.02)
        self.current_lr_time = pulse_time
        self.current_lr_angle = target_angle
        self._limit_angle()

    def turn_up(self, degree):
        if self.status == "sleep":
            return
        target_angle = self.current_ud_angle - degree
        pulse_time = self.current_ud_time - degree * self.pulse_time_per_degree
        self.driver.setServoPulse(UD_CHANNEL, pulse_time)
        time.sleep(0.02)
        self.current_ud_angle = target_angle
        self.current_ud_time = pulse_time
        self._limit_angle()

    def turn_down(self, degree):
        if self.status == "sleep":
            return
        target_angle = self.current_ud_angle + degree
        pulse_time = self.current_ud_time + degree * self.pulse_time_per_degree
        self.driver.setServoPulse(UD_CHANNEL, pulse_time)
        time.sleep(0.02)
        self.current_ud_angle = target_angle
        self.current_ud_time = pulse_time
        self._limit_angle()

    def sleep(self):
        self.driver.sleep()
        self.status = "sleep"

    def wake(self):
        self.driver.wake()
        self.status = "wake"


servo = ServoController()


def turn_up():
    servo.turn_up(3)


def turn_down():
    servo.turn_down(3)


def turn_right():
    servo.turn_right(3)


def turn_left():
    servo.turn_left(3)


def end_turn():
    servo.sleep()


def start_turn():
    servo.wake()


if __name__ == "__main__":
    import pdb;pdb.set_trace()
    turn_up()
    turn_right()
