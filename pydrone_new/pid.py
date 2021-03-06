#!/usr/bin/python3
import os
import time
import pigpio
from mpu6050 import mpu6050
from math import atan, sqrt

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)
pi = pigpio.pi()
mpu = mpu6050(0x68)  # check if it's the right pin


def pid():

    # pins for motors---------------------------------------------------------------------------------------------------
    motor27 = 27  # left1
    motor19 = 19  # left2
    motor20 = 20  # right1
    motor24 = 24  # right2

    # motors start------------------------------------------------------------------------------------------------------
    throttle = 1300
    # motors speed--------------------------------------------------------------------------------------------------

    pi.set_servo_pulsewidth(motor27, 0)
    pi.set_servo_pulsewidth(motor19, 0)
    pi.set_servo_pulsewidth(motor20, 0)
    pi.set_servo_pulsewidth(motor24, 0)

    # elapsed time------------------------------------------------------------------------------------------------------
    elapsed_time = 0.0000001

    # PID constants-----------------------------------------------------------------------------------------------------
    pid_p = 0
    pid_i = 0
    pid_d = 0
    pid_p1 = 0
    pid_i1 = 0
    pid_d1 = 0
    pid_d2 = 0
    pid_i2 = 0
    pid_d2 = 0
    kp_roll = 3.55
    ki_roll = 0.005
    kd_roll = 2.05
    kp_pitch = 3.55
    ki_pitch = 0.005
    kd_pitch = 2.05
    kp_yaw = 3.55
    kd_yaw = 0.005
    ki_yaw = 2.05
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
        accel_angle_z = atan(sqrt(pow(accel_x, 2) + pow(accel_y, 2)) / accel_z) * rad_to_deg

        # gyrometer-----------------------------------------------------------------------------------------------------
        gyro_data = mpu.get_gyro_data()
        gyro_x = gyro_data['x']
        gyro_y = gyro_data['y']
        gyro_z = gyro_data['z']

        # total angle---------------------------------------------------------------------------------------------------
        total_angle = [0, 0, 0]
        total_angle[0] = 0.98 * (total_angle[0] + gyro_x * elapsed_time) + 0.02 * accel_angle_x
        total_angle[1] = 0.98 * (total_angle[1] + gyro_y * elapsed_time) + 0.02 * accel_angle_y
        total_angle[2] = 0.98 * (total_angle[2] + gyro_z * elapsed_time) + 0.02 * accel_angle_z

        # PID for x angle-----------------------------------------------------------------------------------------------
        error = total_angle[0] - desired_angle
        previous_error = error
        pid_p = kp_roll * error  # proportional

        if -3 < error < 3:
            pid_i = pid_i + (ki_roll * error)  # integral
        pid_d = kd_roll * ((error - previous_error) / elapsed_time)  # derivative

        pid_roll = pid_p + pid_i + pid_d

        # PID for y angle-----------------------------------------------------------------------------------------------
        error1 = total_angle[1] - desired_angle
        previous_error1 = error1
        pid_p1 = kp_pitch * error1  # proportional

        if -3 < error1 < 3:
            pid_i1 = pid_i1 + (ki_pitch * error1)    # integral
        pid_d1 = kd_pitch * ((error1 - previous_error1) / elapsed_time)  # derivative

        pid_pitch = pid_p1 + pid_i1 + pid_d1

        # PID for z angle-----------------------------------------------------------------------------------------------

        error2 = total_angle[2] - desired_angle
        previous_error2 = error2
        pid_p2 = kp_yaw * error2  # proportional

        if -3 < error2 < 3:
            pid_i2 = pid_i2 + (ki_yaw * error2)    # integral
        pid_d2 = kd_yaw * ((error2 - previous_error2) / elapsed_time)  # derivative

        pid_yaw = pid_p2 + pid_i2 + pid_d2

        # motors speed--------------------------------------------------------------------------------------------------
        if pid_roll < -1000:
            pid_roll = -1000
        if pid_roll > 1000:
            pid_roll = 1000
        if pid_pitch < -1000:
            pid_pitch = -1000
        if pid_pitch > 1000:
            pid_pitch = 1000
        if pid_yaw < -1000:
            pid_yaw = -1000
        if pid_yaw > 1000:
            pid_yaw = 1000

        throttle24 = throttle + pid_yaw + pid_pitch + pid_roll   # right front
        throttle20 = throttle - pid_yaw + pid_pitch - pid_roll   # right back
        throttle19 = throttle - pid_yaw - pid_pitch + pid_roll   # left back
        throttle27 = throttle + pid_yaw - pid_pitch - pid_roll   # left front

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

        print(throttle27, throttle19, throttle20, throttle24)
        print(accel_angle_x, accel_angle_y)
        print(gyro_x, gyro_y)


if __name__ == "__pid__":
    pid()

