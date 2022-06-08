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

# pins for motors
motor13 = 13
motor18 = 18
motor35 = 35
motor38 = 38


# variables
throttle = 1300
desired_angle = 0
rad_to_deg = 180 / 3.141592654
temp_data = mpu.get_temp()

pi.set_servo_pulsewidth(motor13, throttle)
pi.set_servo_pulsewidth(motor18, throttle)
pi.set_servo_pulsewidth(motor35, throttle)
pi.set_servo_pulsewidth(motor38, throttle)

# PID constants
pid_p = 0
pid_i = 0
pid_d = 0
kp = 3.55
ki = 0.005
kd = 2.05

time_start = time.time()

while True:

    # time
    time_prev = time_start
    time = time.time()
    elapsed_time = time - time_prev

    # accelerometer
    accel_data = mpu.get_accel_data()
    accelX = accel_data['x']
    accelY = accel_data['y']
    accelZ = accel_data['z']

    accel_angle_x = atan(accelY / sqrt(pow(accelX, 2) + pow(accelZ, 2))) * rad_to_deg
    accel_angle_y = atan(accelX / sqrt(pow(accelY, 2) + pow(accelZ, 2))) * rad_to_deg
    accel_angle_z = atan(sqrt(pow(accelX, 2) + pow(accelY, 2)) / accelZ) * rad_to_deg

    # gyrometer
    gyro_data = mpu.get_gyro_data()
    gyroX = gyro_data['x']
    gyroY = gyro_data['y']
    gyroZ = gyro_data['z']

    # total angle
    total_angle = []

    total_angle[0] = 0.98 * (total_angle[0] + gyroX * elapsed_time) + 0.02 * accel_angle_x
    total_angle[1] = 0.98 * (total_angle[1] + gyroY * elapsed_time) + 0.02 * accel_angle_y
    total_angle[2] = 0.98 * (total_angle[2] + gyroZ * elapsed_time) + 0.02 * accel_angle_z

    # PID
    error = total_angle[1] - desired_angle
    previous_error = error
    pid_p = kp * error  # proportional

    if error > -3 & error < 3:
        pid_i = pid_i + (ki * error)    # integral
    pid_d = kd * ((error - previous_error) / elapsed_time)  # derivative

    PID = pid_p + pid_i + pid_d

    if PID < -1000:
        PID = -1000
    if PID > 1000:
        PID = 1000

    throttle13 = throttle + PID
    throttle18 = throttle - PID
    throttle35 = throttle + PID
    throttle38 = throttle - PID

    # left
    if throttle13 < 1000:
        throttlec13 = 1000
    if throttle13 > 2000:
        throttle13 = 2000

    if throttle18 < 1000:
        throttle18 = 1000
    if throttle18 > 2000:
        throttle18 = 2000

    # right
    if throttle35 < 1000:
        throttle35 = 1000
    if throttle35 > 2000:
        throttle35 = 2000

    if throttle38 < 1000:
        throttle38 = 1000
    if throttle38 > 2000:
        throttle38 = 2000

    pi.set_servo_pulsewidth(motor13, throttle13)
    pi.set_servo_pulsewidth(motor18, throttle18)
    pi.set_servo_pulsewidth(motor35, throttle35)
    pi.set_servo_pulsewidth(motor38, throttle38)

    print(throttle13)
    print(throttle18)
    print(throttle35)
    print(throttle38)
