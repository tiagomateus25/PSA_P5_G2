#!/usr/bin/python3
from mpu6050 import mpu6050
import time
from math import atan, sqrt
import os
import pigpio
import readchar
from colorama import Fore, Back, Style
import json
import socket

os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)
pi = pigpio.pi()

mpu = mpu6050(0x68)     # check if it's the right pin


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
            time.sleep(12)
            print('')
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


def controller():
    # variables---------------------------------------------------------------------------------------------------------
    desired_angle = 0
    rad_to_deg = 180 / 3.141592654
    # temp_data = mpu.get_temp()

    pi.set_servo_pulsewidth(motor27, throttle)
    pi.set_servo_pulsewidth(motor19, throttle)
    pi.set_servo_pulsewidth(motor20, throttle)
    pi.set_servo_pulsewidth(motor24, throttle)

    # PID constants-----------------------------------------------------------------------------------------------------
    # pid_p = 0
    pid_i = 0
    # pid_d = 0
    # pid_p1 = 0
    pid_i1 = 0
    # pid_d1 = 0
    kp = 3.55
    ki = 0.005
    kd = 2.05
    while True:

        # time----------------------------------------------------------------------------------------------------------
        elapsed_time = 0.01

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

        if error > -3 & error < 3:
            pid_i = pid_i + (ki * error)  # integral
        pid_d = kd * ((error - previous_error) / elapsed_time)  # derivative

        pid = pid_p + pid_i + pid_d

        if pid < -1000:
            pid = -1000
        if pid > 1000:
            pid = 1000

        throttle27 = throttle + pid
        throttle24 = throttle + pid
        throttle20 = throttle - pid
        throttle19 = throttle - pid

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

        # Motor rotations
        pi.set_servo_pulsewidth(motor27, throttle27)
        pi.set_servo_pulsewidth(motor19, throttle19)
        pi.set_servo_pulsewidth(motor20, throttle20)
        pi.set_servo_pulsewidth(motor24, throttle24)

        # PID for y angle-----------------------------------------------------------------------------------------------
        error1 = total_angle[1] - desired_angle
        previous_error1 = error1
        pid_p1 = kp * error1  # proportional

        if error1 > -3 & error1 < 3:
            pid_i1 = pid_i1 + (ki * error1)    # integral
        pid_d1 = kd * ((error1 - previous_error1) / elapsed_time)  # derivative

        pid1 = pid_p1 + pid_i1 + pid_d1

        if pid1 < -1000:
            pid1 = -1000
        if pid1 > 1000:
            pid1 = 1000

        throttle27 = throttle + pid1
        throttle19 = throttle + pid1
        throttle20 = throttle - pid1
        throttle24 = throttle - pid1

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


def key_control():
    throttle27 = throttle
    throttle19 = throttle
    throttle20 = throttle
    throttle24 = throttle
    print("starting motors")
    time.sleep(5)
    pressed_key = readchar.readkey()
    while True:
        pi.set_servo_pulsewidth(motor27, throttle27)
        pi.set_servo_pulsewidth(motor19, throttle19)
        pi.set_servo_pulsewidth(motor20, throttle20)
        pi.set_servo_pulsewidth(motor24, throttle24)
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

        print('Throttle of motor 27 at' + str(throttle27))
        print('Throttle of motor 19 at' + str(throttle19))
        print('Throttle of motor 20 at' + str(throttle20))
        print('Throttle of motor 24 at' + str(throttle24))

        # controller()


def xbox():
    # Create axis TCP/IP sockets-----------------------------------------------------------------------------------------
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port---------------------------------------------------------------------------------------
    server_address = ('192.168.143.11', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections-----------------------------------------------------------------------------------
    sock.listen(1)

    while True:
        # Wait for axis connection
        print('waiting for axis connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:

                # xbox controllers commands
                data = connection.recv(5000)
                data = json.loads(data.decode())
                axis = data.get("a")
                lt = data.get("b")
                rt = data.get("c")
                print(axis, lt, rt)

                # motors speed

                throttle27 = throttle
                throttle19 = throttle
                throttle20 = throttle
                throttle24 = throttle
                print("starting motors")
                pi.set_servo_pulsewidth(motor27, throttle27)
                pi.set_servo_pulsewidth(motor19, throttle19)
                pi.set_servo_pulsewidth(motor20, throttle20)
                pi.set_servo_pulsewidth(motor24, throttle24)
                if axis == [-1, 0]:  # TODO get correct values
                    throttle27 -= 100
                    throttle19 -= 100
                    throttle20 += 100
                    throttle24 += 100
                if axis == [-1, 0]:  # TODO get correct values
                    throttle27 += 100
                    throttle19 += 100
                    throttle20 -= 100
                    throttle24 -= 100
                if axis == [-1, 0]:  # TODO get correct values
                    throttle27 -= 100
                    throttle19 += 100
                    throttle20 += 100
                    throttle24 -= 100
                if axis == [-1, 0]:  # TODO get correct values
                    throttle27 += 100
                    throttle19 -= 100
                    throttle20 -= 100
                    throttle24 += 100
                if lt == [1]:
                    throttle27 += 100
                    throttle19 += 100
                    throttle20 += 100
                    throttle24 += 100
                if rt == [1]:
                    throttle27 -= 100
                    throttle19 -= 100
                    throttle20 -= 100
                    throttle24 -= 100
        finally:
            # Clean up the connection
            connection.close()


def instructions():

    print(Back.MAGENTA + 'Instructions:' + Style.RESET_ALL + '\n')
    print('If you chose the ' + Back.MAGENTA + 'key' + Style.RESET_ALL + ' option: \n ')
    print('Press ' + Fore.YELLOW + 'a' + Style.RESET_ALL + ' to go left.')
    print('Press ' + Fore.YELLOW + 'd' + Style.RESET_ALL + ' to go right.')
    print('Press ' + Fore.YELLOW + 'w' + Style.RESET_ALL + ' to go in front.')
    print('Press ' + Fore.YELLOW + 's' + Style.RESET_ALL + ' to go back.')
    print('Press ' + Fore.YELLOW + 'spacebar' + Style.RESET_ALL + ' to go up.')
    print('Press ' + Fore.YELLOW + 'c' + Style.RESET_ALL + ' to go down.\n')
    print('If you chose the ' + Back.MAGENTA + 'xbox' + Style.RESET_ALL + ' option: \n')
    print('Use the ' + Fore.YELLOW + 'joystick' + Style.RESET_ALL + ' to control the drone: \n')
    print('Tilt the ' + Fore.YELLOW + 'joystick left' + Style.RESET_ALL + ' to go left.')
    print('Tilt the ' + Fore.YELLOW + 'joystick right' + Style.RESET_ALL + ' to go right.')
    print('Tilt the ' + Fore.YELLOW + 'joystick front' + Style.RESET_ALL + ' to go front.')
    print('Tilt the ' + Fore.YELLOW + 'joystick back' + Style.RESET_ALL + ' to go back.')
    print('Press ' + Fore.YELLOW + 'RT' + Style.RESET_ALL + ' to go up.')
    print('Press ' + Fore.YELLOW + 'LT' + Style.RESET_ALL + ' to go down. \n')

    inp = input()
    if inp == "calibrate":
        print('\n')
        calibrate()
    if inp == "key":
        print('\n')
        key_control()
    if inp == "xbox":
        print('\n')
        xbox()
    if inp == "instructions":
        print('\n')
        instructions()


def main():
    print(Back.MAGENTA + '<--------------------Welcome to the Pydrone alpha version!--------'
                         '------------>' + Style.RESET_ALL + '\n')
    print(Back.MAGENTA + 'List of commands:' + Style.RESET_ALL + '\n')
    print('Type ' + Fore.RED + 'instructions' + Style.RESET_ALL + ' in the terminal '
                                                                  'and press Enter for the instructions list.')
    print('Type ' + Fore.RED + 'calibrate' + Style.RESET_ALL + ' in the terminal '
                                                               'and press Enter for the calibration of the ESCs.')
    print('Type ' + Fore.RED + 'key' + Style.RESET_ALL + ' in the terminal '
                                                         'and press Enter to control the drone with the keyboard.')
    print('Type ' + Fore.RED + 'xbox' + Style.RESET_ALL + ' in the terminal '
                                                          'and press Enter to '
                                                          'control the drone with the xbox controller. \n')
    print('Press' + Fore.RED + 'Ctrl-C' + Style.RESET_ALL + 'to quit.\n')
    print(Back.MAGENTA + 'Suggestions:' + Style.RESET_ALL + '\n')
    print('Start off with the ' + Fore.RED + 'calibrate' + Style.RESET_ALL + ' command if this is '
                                                                             'your first time flying Pydrone. \n')
    print('Learn how to control the drone with the ' + Fore.RED + 'instructions' + Style.RESET_ALL + ' command. \n')

    inp = input()
    if inp == "calibrate":
        print('\n')
        calibrate()
    if inp == "key":
        print('\n')
        key_control()
        controller()
    if inp == "xbox":
        print('\n')
        xbox()
        controller()
    if inp == "instructions":
        print('\n')
        instructions()


if __name__ == "__main__":
    main()
