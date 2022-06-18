#!/usr/bin/python3
import os
import pigpio
import time
os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)
pi = pigpio.pi()

# pins for motors-------------------------------------------------------------------------------------------------------
motor27 = 27    # left1
motor19 = 19    # left2
motor20 = 20    # right1
motor24 = 24    # right2

# motors speed----------------------------------------------------------------------------------------------------------
throttle = 1300


def calibrate():  # This is the auto calibration procedure of a normal ESC

    print('You have chosen ESCs calibration. Follow the instructions to proceed.')
    time.sleep(3)
    max_value = 2400  # change this if your ESC's max value is different or leave it
    min_value = 700  # change this if your ESC's min value is different or leave it
    pi.set_servo_pulsewidth(motor27, 0)
    pi.set_servo_pulsewidth(motor19, 0)
    pi.set_servo_pulsewidth(motor20, 0)
    pi.set_servo_pulsewidth(motor24, 0)
    print("Disconnect the battery and press Enter")
    inp_a = input()
    if inp_a == '':
        pi.set_servo_pulsewidth(motor27, max_value)
        pi.set_servo_pulsewidth(motor19, max_value)
        pi.set_servo_pulsewidth(motor20, max_value)
        pi.set_servo_pulsewidth(motor24, max_value)
        print("Connect the battery. Maximum speed is being acquired, wait for the next instruction.")
        time.sleep(20)
        print('Press Enter to continue.')
        inp_b = input()
        if inp_b == '':
            pi.set_servo_pulsewidth(motor27, min_value)
            pi.set_servo_pulsewidth(motor19, min_value)
            pi.set_servo_pulsewidth(motor20, min_value)
            pi.set_servo_pulsewidth(motor24, min_value)
            print('Minimum speed is being acquired.')
            time.sleep(7)
            time.sleep(5)
            pi.set_servo_pulsewidth(motor27, 0)
            pi.set_servo_pulsewidth(motor19, 0)
            pi.set_servo_pulsewidth(motor20, 0)
            pi.set_servo_pulsewidth(motor24, 0)
            time.sleep(2)
            print('Arming ESCs.')
            pi.set_servo_pulsewidth(motor27, min_value)
            pi.set_servo_pulsewidth(motor19, min_value)
            pi.set_servo_pulsewidth(motor20, min_value)
            pi.set_servo_pulsewidth(motor24, min_value)
            time.sleep(1)
            print('Calibration complete.')
            control()


def control():
    time.sleep(1)
    while True:
        pi.set_servo_pulsewidth(motor27, throttle)
        pi.set_servo_pulsewidth(motor19, throttle)
        pi.set_servo_pulsewidth(motor20, throttle)
        pi.set_servo_pulsewidth(motor24, throttle)


inp = input()
if inp == "calibrate":
    calibrate()
    print("ok")

