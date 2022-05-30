#!/usr/bin/env python3
import time
import pygame

# -----------------------------------------
# Initialization
# -----------------------------------------
pygame.init()
pygame.joystick.init()  # Initialize the joysticks.

# Get count of joysticks.
joystick_count = pygame.joystick.get_count()
print('Found ' + str(joystick_count) + ' joysticks.')

# init joystick
joystick = pygame.joystick.Joystick(0)  # Assuming we have only one
joystick.init()

# Get the name from the OS for the controller/joystick.
joystick_name = joystick.get_name()
print('Connected to ' + joystick_name)

number_axes = joystick.get_numaxes()



# -----------------------------------------
# Execution (in cycle)
# -----------------------------------------
while True:
    axis0 = round(joystick.get_axis(0) * 100) / 100
    axis1 = round(joystick.get_axis(1) * 100) / 100
    print('Axis0=' + str(axis0) + '   Axis1=' + str(axis1))
    pygame.event.pump()
    # time.sleep(0.01)

# -----------------------------------------
# Termination
# -----------------------------------------
pygame.quit()
