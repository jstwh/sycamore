"""
This entire file is deprecated, walking engine will be made at some point.
"""

import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

for i in range(2):
    kit.servo[i].set_pulse_width_range(500, 2500)


def init_servos():
    try:
        kit.servo[0].angle = 0
        kit.servo[1].angle = 0
        print("Servos initialized")
    except:
        ValueError("Did you connect your servos to gates 1 and 2?")


def walk():
    while True:
        kit.servo[0].angle = 0
        kit.servo[1].angle = 0
        time.sleep(0.3)
        kit.servo[0].angle = 45
        kit.servo[1].angle = 0
        time.sleep(0.3)
        kit.servo[0].angle = 45
        kit.servo[1].angle = 45
        time.sleep(0.3)
        kit.servo[0].angle = 0
        kit.servo[1].angle = 45
        time.sleep(0.3)
