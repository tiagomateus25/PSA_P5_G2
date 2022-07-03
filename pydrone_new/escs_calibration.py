#!/usr/bin/python3
import os
import time
import pigpio
from mpu6050 import mpu6050


os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)
pi = pigpio.pi()
mpu = mpu6050(0x68)     # check if it's the right pin

# elapsed time----------------------------------------------------------------------------------------------------------
elapsed_time = 0.01
# motors speed----------------------------------------------------------------------------------------------------------
throttle = 1300

# pins for motors-------------------------------------------------------------------------------------------------------
motor27 = 27  # left1
motor19 = 19  # left2
motor20 = 20  # right1
motor24 = 24  # right2

# motors start----------------------------------------------------------------------------------------------------------
pi.set_servo_pulsewidth(motor27, 0)
pi.set_servo_pulsewidth(motor19, 0)
pi.set_servo_pulsewidth(motor20, 0)
pi.set_servo_pulsewidth(motor24, 0)


def calibration():

    print('You have chosen ESCs calibration. Follow the instructions to proceed.\n')
    max_value = 2000  # change this if your ESC's max value is different or leave it
    min_value = 1000  # change this if your ESC's min value is different or leave it
    print('Disconnect the battery and press Enter.\n')
    inp_a = input()
    if inp_a == '':
        pi.set_servo_pulsewidth(motor27, max_value)
        pi.set_servo_pulsewidth(motor19, max_value)
        pi.set_servo_pulsewidth(motor20, max_value)
        pi.set_servo_pulsewidth(motor24, max_value)
        print('Connect the battery. Maximum speed is being acquired, wait for the next instruction.\n')
        time.sleep(12)
        print('Press Enter to continue.\n')
        inp_b = input()
        if inp_b == '':
            pi.set_servo_pulsewidth(motor27, min_value)
            pi.set_servo_pulsewidth(motor19, min_value)
            pi.set_servo_pulsewidth(motor20, min_value)
            pi.set_servo_pulsewidth(motor24, min_value)
            print('Minimum speed is being acquired.\n')
            time.sleep(7)
            time.sleep(5)
            pi.set_servo_pulsewidth(motor27, 0)
            pi.set_servo_pulsewidth(motor19, 0)
            pi.set_servo_pulsewidth(motor20, 0)
            pi.set_servo_pulsewidth(motor24, 0)
            time.sleep(2)
            print('Arming ESCs.\n')
            pi.set_servo_pulsewidth(motor27, min_value)
            pi.set_servo_pulsewidth(motor19, min_value)
            pi.set_servo_pulsewidth(motor20, min_value)
            pi.set_servo_pulsewidth(motor24, min_value)
            time.sleep(1)
            print('Calibration complete. \n')


if __name__ == "__calibration__":
    calibration()
