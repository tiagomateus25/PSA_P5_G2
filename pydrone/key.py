#!/usr/bin/python3
import os
import pigpio
import time
import readchar

os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)
pi = pigpio.pi()


def key_control():

    time.sleep(1)
    # pins for motors---------------------------------------------------------------------------------------------------
    throttle = 1500
    motor27 = 27  # left1
    motor19 = 19  # left2
    motor20 = 20  # right1
    motor24 = 24  # right2
    throttle27 = throttle
    throttle19 = throttle
    throttle20 = throttle
    throttle24 = throttle
    print('starting motors')
    time.sleep(5)
    while True:
        pressed_key = readchar.readkey()
        if pressed_key == chr(97):     # left, a
            throttle27 -= 100
            throttle19 -= 100
            throttle20 += 100
            throttle24 += 100
        if pressed_key == chr(100):    # right, d
            throttle27 += 100
            throttle19 += 100
            throttle20 -= 100
            throttle24 -= 100
        if pressed_key == chr(119):    # front, w
            throttle27 -= 100
            throttle19 += 100
            throttle20 += 100
            throttle24 -= 100
        if pressed_key == chr(100):    # back, s
            throttle27 += 100
            throttle19 -= 100
            throttle20 -= 100
            throttle24 += 100
        if pressed_key == chr(32):     # up, spacebar
            throttle27 += 100
            throttle19 += 100
            throttle20 += 100
            throttle24 += 100
        if pressed_key == chr(99):     # down, c
            throttle27 -= 100
            throttle19 -= 100
            throttle20 -= 100
            throttle24 -= 100
        pi.set_servo_pulsewidth(motor27, throttle27)
        pi.set_servo_pulsewidth(motor19, throttle19)
        pi.set_servo_pulsewidth(motor20, throttle20)
        pi.set_servo_pulsewidth(motor24, throttle24)

        print('Throttle of motor 27 at' + str(throttle27))
        print('Throttle of motor 19 at' + str(throttle19))
        print('Throttle of motor 20 at' + str(throttle20))
        print('Throttle of motor 24 at' + str(throttle24))
        if pressed_key == chr(27):
            quit()
        # controller():


if __name__ == "__key_control__":
    key_control()
