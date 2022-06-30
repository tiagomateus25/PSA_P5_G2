#!/usr/bin/python3
import os
import time
import pigpio
from mpu6050 import mpu6050
import readchar


def key():

    os.system("sudo pigpiod")  # Launching GPIO library
    time.sleep(1)
    pi = pigpio.pi()
    mpu = mpu6050(0x68)  # check if it's the right pin

    # pins for motors---------------------------------------------------------------------------------------------------
    motor27 = 27  # left1
    motor19 = 19  # left2
    motor20 = 20  # right1
    motor24 = 24  # right2

    # motors start------------------------------------------------------------------------------------------------------
    throttle = 1300
    throttle27 = throttle
    throttle19 = throttle
    throttle20 = throttle
    throttle24 = throttle
    # motors speed--------------------------------------------------------------------------------------------------

    pi.set_servo_pulsewidth(motor27, 0)
    pi.set_servo_pulsewidth(motor19, 0)
    pi.set_servo_pulsewidth(motor20, 0)
    pi.set_servo_pulsewidth(motor24, 0)


    while True:

        if readchar.readkey() == chr(97):  # left, a
            throttle27 -= 50
            throttle19 -= 50
            throttle20 += 50
            throttle24 += 50
        if readchar.readkey() == chr(100):  # right, d
            throttle27 += 50
            throttle19 += 50
            throttle20 -= 50
            throttle24 -= 50
        if readchar.readkey() == chr(119):  # front, w
            throttle27 -= 50
            throttle19 += 50
            throttle20 += 50
            throttle24 -= 50
        if readchar.readkey() == chr(115):  # back, s
            throttle27 += 50
            throttle19 -= 50
            throttle20 -= 50
            throttle24 += 50
        if readchar.readkey() == chr(32):  # up, spacebar
            throttle27 += 50
            throttle19 += 50
            throttle20 += 50
            throttle24 += 50
        if readchar.readkey() == chr(99):  # down, c
            throttle27 -= 50
            throttle19 -= 50
            throttle20 -= 50
            throttle24 -= 50
            pi.set_servo_pulsewidth(motor27, throttle27)
            pi.set_servo_pulsewidth(motor19, throttle19)
            pi.set_servo_pulsewidth(motor20, throttle20)
            pi.set_servo_pulsewidth(motor24, throttle24)
        if readchar.readkey() == chr(114):  # throttle 1500, r
            throttle27 = 1500
            throttle19 = 1500
            throttle20 = 1500
            throttle24 = 1500
        # left
        if throttle27 < 1000:
            throttle27 = 1000
        if throttle27 > 2000:
            throttle27 = 2000

        if throttle19 < 1000:
            throttle19 = 1000
        if throttle19 > 2000:
            throttle19 = 2000

        # right
        if throttle20 < 1000:
            throttle20 = 1000
        if throttle20 > 2000:
            throttle20 = 2000

        if throttle24 < 1000:
            throttle24 = 1000
        if throttle24 > 2000:
            throttle24 = 2000

        pi.set_servo_pulsewidth(motor27, throttle27)
        pi.set_servo_pulsewidth(motor19, throttle19)
        pi.set_servo_pulsewidth(motor20, throttle20)
        pi.set_servo_pulsewidth(motor24, throttle24)

        print(throttle27)
        print(throttle19)
        print(throttle20)
        print(throttle24)


if __name__ == "__controller_key__":
    key()
