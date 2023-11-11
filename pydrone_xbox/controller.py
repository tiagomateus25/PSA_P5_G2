#!/usr/bin/python3
import pygame
import time
import os
import pigpio

os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)
pi = pigpio.pi()

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


def controller():
    # Initialization----------------------------------------------------------------------------------------------------
    pygame.init()
    pygame.joystick.init()

    # Get count of joysticks--------------------------------------------------------------------------------------------
    joystick_count = pygame.joystick.get_count()
    print('Found ' + str(joystick_count) + ' joysticks.')

    # init joystick-----------------------------------------------------------------------------------------------------
    joystick = pygame.joystick.Joystick(0)  # Assuming we have only one
    joystick.init()

    # Get the name from the OS for the controller/joystick--------------------------------------------------------------
    joystick_name = joystick.get_name()
    print('Connected to ' + joystick_name)

    number_axes = joystick.get_numaxes()

    while True:
        axis0 = round(joystick.get_axis(0))
        axis1 = round(joystick.get_axis(1))
        lt = round(joystick.get_axis(2))
        rt = round(joystick.get_axis(5))
        pygame.event.pump()

        while lt == 1:
            pi.set_servo_pulsewidth(motor27, 1100)
            pi.set_servo_pulsewidth(motor19, 1100)
            pi.set_servo_pulsewidth(motor20, 1100)
            pi.set_servo_pulsewidth(motor24, 1100)
        while rt == 1:
            pi.set_servo_pulsewidth(motor27, 1200)
            pi.set_servo_pulsewidth(motor19, 1200)
            pi.set_servo_pulsewidth(motor20, 1200)
            pi.set_servo_pulsewidth(motor24, 1200)
        while axis0 == 0 and axis1 == -1:
            pi.set_servo_pulsewidth(motor27, 1100)
            pi.set_servo_pulsewidth(motor19, 1100)
            pi.set_servo_pulsewidth(motor20, 1200)
            pi.set_servo_pulsewidth(motor24, 1200)
        while axis0 == 0 and axis1 == 1:
            pi.set_servo_pulsewidth(motor27, 1200)
            pi.set_servo_pulsewidth(motor19, 1200)
            pi.set_servo_pulsewidth(motor20, 1200)
            pi.set_servo_pulsewidth(motor24, 1200)
        while axis0 == -1 and axis1 == 0:
            pi.set_servo_pulsewidth(motor27, 1200)
            pi.set_servo_pulsewidth(motor19, 1200)
            pi.set_servo_pulsewidth(motor20, 1200)
            pi.set_servo_pulsewidth(motor24, 1200)
        while axis0 == 1 and axis1 == 0:
            pi.set_servo_pulsewidth(motor27, 1200)
            pi.set_servo_pulsewidth(motor19, 1200)
            pi.set_servo_pulsewidth(motor20, 1200)
            pi.set_servo_pulsewidth(motor24, 1200)


if __name__ == "__controller__":
    controller()
