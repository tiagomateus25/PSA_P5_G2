#!/usr/bin/python3
from colorama import Fore, Back, Style
import os
import time
import pigpio
from mpu6050 import mpu6050
from key_pid import controller_key
from xbox_pid import controller_xbox
from key import key
from xbox import xbox

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

    inp = input()
    if inp == 'calibration':
        print('\n')
        calibration()
    if inp == 'keypid':
        controller_key()
    if inp == 'xboxpid':
        controller_xbox()
    if inp == 'instructions':
        print('\n')
        instructions()
    if inp == 'key':
        print('\n')
        key()
    if inp == 'xbox':
        print('\n')
        xbox()


def instructions():

    print(Back.MAGENTA + 'Instructions:' + Style.RESET_ALL + '\n')
    print('If you chose the ' + Back.MAGENTA + 'key' + Style.RESET_ALL + ' option: \n ')
    print('Press ' + Fore.YELLOW + 'a' + Style.RESET_ALL + ' to go left.')
    print('Press ' + Fore.YELLOW + 'd' + Style.RESET_ALL + ' to go right.')
    print('Press ' + Fore.YELLOW + 'w' + Style.RESET_ALL + ' to go in front.')
    print('Press ' + Fore.YELLOW + 's' + Style.RESET_ALL + ' to go back.')
    print('Press ' + Fore.YELLOW + 'spacebar' + Style.RESET_ALL + ' to go up.')
    print('Press ' + Fore.YELLOW + 'c' + Style.RESET_ALL + ' to go down.')
    print('Press ' + Fore.YELLOW + 'r' + Style.RESET_ALL + ' to stabilize.\n')
    print('If you chose the ' + Back.MAGENTA + 'xbox' + Style.RESET_ALL + ' option: \n')
    print('Use the ' + Fore.YELLOW + 'joystick' + Style.RESET_ALL + ' to control the drone: \n')
    print('Tilt the ' + Fore.YELLOW + 'joystick left' + Style.RESET_ALL + ' to go left.')
    print('Tilt the ' + Fore.YELLOW + 'joystick right' + Style.RESET_ALL + ' to go right.')
    print('Tilt the ' + Fore.YELLOW + 'joystick front' + Style.RESET_ALL + ' to go front.')
    print('Tilt the ' + Fore.YELLOW + 'joystick back' + Style.RESET_ALL + ' to go back.')
    print('Press ' + Fore.YELLOW + 'RT' + Style.RESET_ALL + ' to go up.')
    print('Press ' + Fore.YELLOW + 'LT' + Style.RESET_ALL + ' to go down. \n')

    inp = input()
    if inp == 'calibration':
        print('\n')
        calibration()
    if inp == 'keypid':
        print('\n')
        controller_key()
    if inp == 'xboxpid':
        print('\n')
        controller_xbox()
    if inp == 'instructions':
        print('\n')
        instructions()
    if inp == 'key':
        print('\n')
        key()
    if inp == 'xbox':
        print('\n')
        xbox()


def main():
    print(Back.MAGENTA + '<--------------------Welcome to the Pydrone alpha version!--------'
                         '------------>' + Style.RESET_ALL + '\n')
    print(Back.MAGENTA + 'List of commands:' + Style.RESET_ALL + '\n')
    print('Type ' + Fore.RED + 'instructions' + Style.RESET_ALL + ' in the terminal '
                                                                  'and press Enter for the instructions list.')
    print('Type ' + Fore.RED + 'calibration' + Style.RESET_ALL + ' in the terminal '
                                                                 'and press Enter for the calibration of the ESCs.')
    print('Type ' + Fore.RED + 'key' + Style.RESET_ALL + ' to control the drone with the keyboard, after '
                                                         'calibration is complete.')
    print('Type ' + Fore.RED + 'xbox' + Style.RESET_ALL + ' to control the drone with the xbox controller, after '
                                                          'calibration is complete. \n')
    print('Press ' + Fore.RED + 'Ctrl-C' + Style.RESET_ALL + ' to quit.\n')
    print(Back.MAGENTA + 'Suggestions:' + Style.RESET_ALL + '\n')
    print('Start off with the ' + Fore.RED + 'calibration' + Style.RESET_ALL + ' command if this is '
                                                                               'your first time flying Pydrone. \n')
    print('Learn how to control the drone with the ' + Fore.RED + 'instructions' + Style.RESET_ALL + ' command. \n')

    inp = input()
    if inp == 'calibration':
        print('\n')
        calibration()
    if inp == 'key':
        print('\n')
        controller_key()
    if inp == 'xboxpid':
        print('\n')
        controller_xbox()
    if inp == 'instructions':
        print('\n')
        instructions()
    if inp == 'key':
        print('\n')
        key()
    if inp == 'xbox':
        print('\n')
        xbox()


if __name__ == "__main__":
    main()
