#!/usr/bin/python3
from mpu6050 import mpu6050
import time
from math import atan, sqrt
import os
import pigpio

os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)

mpu = mpu6050(0x68)     # check if it's the right pin

pi = pigpio.pi()

# pins for motors-------------------------------------------------------------------------------------------------------
motor27 = 27    # left1
motor19 = 19    # left2
motor20 = 20    # right1
motor24 = 24    # right2


# variables-------------------------------------------------------------------------------------------------------------
throttle = 1300
desired_angle = 0
rad_to_deg = 180 / 3.141592654
temp_data = mpu.get_temp()

pi.set_servo_pulsewidth(motor27, throttle)
pi.set_servo_pulsewidth(motor19, throttle)
pi.set_servo_pulsewidth(motor20, throttle)
pi.set_servo_pulsewidth(motor24, throttle)

# PID constants---------------------------------------------------------------------------------------------------------
pid_p = 0
pid_i = 0
pid_d = 0
pid_p1 = 0
pid_i1 = 0
pid_d1 = 0
kp = 3.55
ki = 0.005
kd = 2.05

time_start = time.time()

while True:

    # time--------------------------------------------------------------------------------------------------------------
    time_prev = time_start
    time = time.time()
    elapsed_time = time - time_prev

    # accelerometer-----------------------------------------------------------------------------------------------------
    accel_data = mpu.get_accel_data()
    accelX = accel_data['x']
    accelY = accel_data['y']
    accelZ = accel_data['z']

    accel_angle_x = atan(accelY / sqrt(pow(accelX, 2) + pow(accelZ, 2))) * rad_to_deg   # pitch
    accel_angle_y = atan(-accelX / sqrt(pow(accelY, 2) + pow(accelZ, 2))) * rad_to_deg  # roll
    # accel_angle_z = atan(sqrt(pow(accelX, 2) + pow(accelY, 2)) / accelZ) * rad_to_deg

    # gyrometer---------------------------------------------------------------------------------------------------------
    gyro_data = mpu.get_gyro_data()
    gyroX = gyro_data['x']
    gyroY = gyro_data['y']
    gyroZ = gyro_data['z']

    # total angle-------------------------------------------------------------------------------------------------------
    total_angle = []
    total_angle[0] = 0.98 * (total_angle[0] + gyroX * elapsed_time) + 0.02 * accel_angle_x
    total_angle[1] = 0.98 * (total_angle[1] + gyroY * elapsed_time) + 0.02 * accel_angle_y
    # total_angle[2] = 0.98 * (total_angle[2] + gyroZ * elapsed_time) + 0.02 * accel_angle_z

    # PID for x angle---------------------------------------------------------------------------------------------------
    error = total_angle[0] - desired_angle
    previous_error = error
    pid_p = kp * error  # proportional

    if error > -3 & error < 3:
        pid_i = pid_i + (ki * error)  # integral
    pid_d = kd * ((error - previous_error) / elapsed_time)  # derivative

    PID = pid_p + pid_i + pid_d

    if PID < -1000:
        PID = -1000
    if PID > 1000:
        PID = 1000

    throttle27 = throttle + PID
    throttle24 = throttle + PID
    throttle20 = throttle - PID
    throttle19 = throttle - PID

    # front
    if throttle27 < 1000:
        throttle27 = 1000
    if throttle27 > 2000:
        throttle27 = 2000

    if throttle24 < 1000:
        throttle24 = 1000
    if throttle24 > 2000:
        throttle24 = 2000

    # back
    if throttle20 < 1000:
        throttle20 = 1000
    if throttle20 > 2000:
        throttle20 = 2000

    if throttle19 < 1000:
        throttle19 = 1000
    if throttle19 > 2000:
        throttle19 = 2000

    # # Motor rotations
    # pi.set_servo_pulsewidth(motor27, throttle27)
    # pi.set_servo_pulsewidth(motor19, throttle19)
    # pi.set_servo_pulsewidth(motor20, throttle20)
    # pi.set_servo_pulsewidth(motor24, throttle24)

    # PID for y angle---------------------------------------------------------------------------------------------------
    error1 = total_angle[1] - desired_angle
    previous_error1 = error1
    pid_p1 = kp * error1  # proportional

    if error1 > -3 & error1 < 3:
        pid_i1 = pid_i1 + (ki * error1)    # integral
    pid_d1 = kd * ((error1 - previous_error1) / elapsed_time)  # derivative

    PID1 = pid_p1 + pid_i1 + pid_d1

    if PID1 < -1000:
        PID1 = -1000
    if PID1 > 1000:
        PID1 = 1000

    throttle27 = throttle + PID1
    throttle19 = throttle + PID1
    throttle20 = throttle - PID1
    throttle24 = throttle - PID1

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

    # Motor rotations
    pi.set_servo_pulsewidth(motor27, throttle27)
    pi.set_servo_pulsewidth(motor19, throttle19)
    pi.set_servo_pulsewidth(motor20, throttle20)
    pi.set_servo_pulsewidth(motor24, throttle24)

