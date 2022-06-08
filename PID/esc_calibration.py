#!/usr/bin/python3
import time
import os
import pigpio

os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)   # As I said it is too impatient and so if this delay is removed you will get an error
pi = pigpio.pi()

ESC = 4  # Connect the ESC in this GPIO pin
pi.set_servo_pulsewidth(ESC, 0)

max_value = 2000    # change this if your ESC's max value is different or leave it
min_value = 700     # change this if your ESC's min value is different or leave it


def calibrate():   # This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW...you will here two beeps, then wait for a gradual"
              " falling tone then press Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, min_value)
            print("Wierd eh! Special tone")
            time.sleep(7)
            print("Wait for it ....")
            time.sleep(5)
            print("Im working on it, DONT WORRY JUST WAIT.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print("Finished")
