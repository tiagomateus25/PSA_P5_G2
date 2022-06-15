#!/usr/bin/python3
import time
import os
import pigpio

os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)   # As I said it is too impatient and so if this delay is removed you will get an error
pi = pigpio.pi()

motor27 = 27  # Connect the ESC in this GPIO pin
motor19 = 19
motor20 = 20
motor24 = 24

pi.set_servo_pulsewidth(motor27, 0)
pi.set_servo_pulsewidth(motor19, 0)
pi.set_servo_pulsewidth(motor20, 0)
pi.set_servo_pulsewidth(motor24, 0)

max_value = 2400    # change this if your ESC's max value is different or leave it
min_value = 700     # change this if your ESC's min value is different or leave it


def calibrate():   # This is the auto calibration procedure of a normal ESC

    pi.set_servo_pulsewidth(motor27, 0)
    pi.set_servo_pulsewidth(motor19, 0)
    pi.set_servo_pulsewidth(motor20, 0)
    pi.set_servo_pulsewidth(motor24, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(motor27, max_value)
        pi.set_servo_pulsewidth(motor19, max_value)
        pi.set_servo_pulsewidth(motor20, max_value)
        pi.set_servo_pulsewidth(motor24, max_value)
        print("Connect the battery NOW...you will here two beeps, then wait for a gradual"
              " falling tone then press Enter")
        time.sleep(20)
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(motor27, min_value)
            pi.set_servo_pulsewidth(motor19, min_value)
            pi.set_servo_pulsewidth(motor20, min_value)
            pi.set_servo_pulsewidth(motor24, min_value)
            print("Wierd eh! Special tone")
            time.sleep(7)
            print("Wait for it ....")
            time.sleep(5)
            print("Im working on it, DONT WORRY JUST WAIT.....")
            pi.set_servo_pulsewidth(motor27, 0)
            pi.set_servo_pulsewidth(motor19, 0)
            pi.set_servo_pulsewidth(motor20, 0)
            pi.set_servo_pulsewidth(motor24, 0)
            time.sleep(2)
            print("Arming ESC now...")
            pi.set_servo_pulsewidth(motor27, min_value)
            pi.set_servo_pulsewidth(motor19, min_value)
            pi.set_servo_pulsewidth(motor20, min_value)
            pi.set_servo_pulsewidth(motor24, min_value)
            time.sleep(1)
            print("Finished")


def control():
    speed = 1500
    print("starting old_motors_code")
    time.sleep(5)
    inp = input()
    while True:
        pi.set_servo_pulsewidth(motor27, speed)
        pi.set_servo_pulsewidth(motor19, speed)
        pi.set_servo_pulsewidth(motor20, speed)
        pi.set_servo_pulsewidth(motor24, speed)
        if inp == "a":
            speed += 100
        if inp == "d":
            speed -= 100


inp = input()
if inp == "calibrate":
    calibrate()
elif inp == "control":
    control()
