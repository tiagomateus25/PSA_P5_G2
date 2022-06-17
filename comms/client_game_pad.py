#!/usr/bin/python3
# socket_echo_client.py

import socket
import sys
import pygame
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

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

while True:

    axis0 = round(joystick.get_axis(0) * 100) / 100
    axis1 = round(joystick.get_axis(1) * 100) / 100
    axis2 = round(joystick.get_axis(2) * 100) / 100
    axis3 = round(joystick.get_axis(3) * 100) / 100
    pygame.event.pump()
    # Send data
    message = str((str(axis0), str(axis1)))
    message1 = str((str(axis2), str(axis3)))
    print(message, message1)

    byt1 = message.encode()
    byt2 = message.encode()

    sock.send(byt1)




