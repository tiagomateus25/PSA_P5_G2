#!/usr/bin/python3
import os
import time
import pigpio
from mpu6050 import mpu6050
from math import atan, sqrt
import readchar


def controller_key():

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
    pi.set_servo_pulsewidth(motor27, 0)
    pi.set_servo_pulsewidth(motor19, 0)
    pi.set_servo_pulsewidth(motor20, 0)
    pi.set_servo_pulsewidth(motor24, 0)

    # elapsed time------------------------------------------------------------------------------------------------------
    elapsed_time = 0.0001

    # PID constants-----------------------------------------------------------------------------------------------------
    pid = 0
    pid1 = 0
    pid_p = 0
    pid_i = 0
    pid_d = 0
    pid_p1 = 0
    pid_i1 = 0
    pid_d1 = 0
    kp = 3.55
    ki = 0.005
    kd = 2.05

    # motors speed------------------------------------------------------------------------------------------------------
    throttle = 1300
    throttle24 = throttle - pid - pid1  # right front
    throttle20 = throttle - pid + pid1  # right back
    throttle19 = throttle + pid + pid1  # left back
    throttle27 = throttle + pid - pid1  # left front

    # desired angle-----------------------------------------------------------------------------------------------------
    desired_angle = 0

    # radians to degree coefficient-------------------------------------------------------------------------------------
    rad_to_deg = 180 / 3.141592654

    while True:

        # accelerometer-------------------------------------------------------------------------------------------------
        accel_data = mpu.get_accel_data()
        accel_x = accel_data['x']
        accel_y = accel_data['y']
        accel_z = accel_data['z']

        accel_angle_x = atan(accel_y / sqrt(pow(accel_x, 2) + pow(accel_z, 2))) * rad_to_deg   # pitch
        accel_angle_y = atan(-accel_x / sqrt(pow(accel_y, 2) + pow(accel_z, 2))) * rad_to_deg  # roll
        # accel_angle_z = atan(sqrt(pow(accel_x, 2) + pow(accel_y, 2)) / accel_z) * rad_to_deg

        # gyrometer-----------------------------------------------------------------------------------------------------
        gyro_data = mpu.get_gyro_data()
        gyro_x = gyro_data['x']
        gyro_y = gyro_data['y']
        # gyro_z = gyro_data['z']

        # total angle---------------------------------------------------------------------------------------------------
        total_angle = [0, 0, 0]
        total_angle[0] = 0.98 * (total_angle[0] + gyro_x * elapsed_time) + 0.02 * accel_angle_x
        total_angle[1] = 0.98 * (total_angle[1] + gyro_y * elapsed_time) + 0.02 * accel_angle_y
        # total_angle[2] = 0.98 * (total_angle[2] + gyro_z * elapsed_time) + 0.02 * accel_angle_z

        # PID for x angle-----------------------------------------------------------------------------------------------
        error = total_angle[0] - desired_angle
        previous_error = error
        pid_p = kp * error  # proportional

        if -3 < error < 3:
            pid_i = pid_i + (ki * error)  # integral
        pid_d = kd * ((error - previous_error) / elapsed_time)  # derivative

        pid = pid_p + pid_i + pid_d

        if pid < -1000:
            pid = -1000
        if pid > 1000:
            pid = 1000

        # PID for y angle-----------------------------------------------------------------------------------------------
        error1 = total_angle[1] - desired_angle
        previous_error1 = error1
        pid_p1 = kp * error1  # proportional

        if -3 < error1 < 3:
            pid_i1 = pid_i1 + (ki * error1)    # integral
        pid_d1 = kd * ((error1 - previous_error1) / elapsed_time)  # derivative

        pid1 = pid_p1 + pid_i1 + pid_d1

        if pid1 < -1000:
            pid1 = -1000
        if pid1 > 1000:
            pid1 = 1000

        pressed_key = readchar.readkey()
        if pressed_key == chr(97):  # left, a
            throttle27 -= 50
            throttle19 -= 50
            throttle20 += 50
            throttle24 += 50
        if pressed_key == chr(100):  # right, d
            throttle27 += 50
            throttle19 += 50
            throttle20 -= 50
            throttle24 -= 50
        if pressed_key == chr(119):  # front, w
            throttle27 -= 50
            throttle19 += 50
            throttle20 += 50
            throttle24 -= 50
        if pressed_key == chr(100):  # back, s
            throttle27 += 50
            throttle19 -= 50
            throttle20 -= 50
            throttle24 += 50
        if pressed_key == chr(32):  # up, spacebar
            throttle27 += 50
            throttle19 += 50
            throttle20 += 50
            throttle24 += 50
        if pressed_key == chr(99):  # down, c
            throttle27 -= 50
            throttle19 -= 50
            throttle20 -= 50
            throttle24 -= 50
        if pressed_key == chr(114):  # throttle 1500, r
            throttle27 = 1500
            throttle19 = 1500
            throttle20 = 1500
            throttle24 = 1500

        pi.set_servo_pulsewidth(motor27, throttle27)
        pi.set_servo_pulsewidth(motor19, throttle19)
        pi.set_servo_pulsewidth(motor20, throttle20)
        pi.set_servo_pulsewidth(motor24, throttle24)

        print(throttle27)
        print(throttle19)
        print(throttle20)
        print(throttle24)

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


if __name__ == "__controller_key__":
    controller_key()
