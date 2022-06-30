#!/usr/bin/python3
import socket
import json
import pygame
import time


# Create a TCP/IP socket------------------------------------------------------------------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening----------------------------------------------------------
server_address = ('192.168.143.11', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# Initialization--------------------------------------------------------------------------------------------------------
pygame.init()
pygame.joystick.init()

# Get count of joysticks------------------------------------------------------------------------------------------------
joystick_count = pygame.joystick.get_count()
print('Found ' + str(joystick_count) + ' joysticks.')

# init joystick---------------------------------------------------------------------------------------------------------
joystick = pygame.joystick.Joystick(0)  # Assuming we have only one
joystick.init()

# Get the name from the OS for the controller/joystick------------------------------------------------------------------
joystick_name = joystick.get_name()
print('Connected to ' + joystick_name)

while True:
    axis0 = int(round(joystick.get_axis(0)))
    axis1 = int(round(joystick.get_axis(1)))
    lt = int(round(joystick.get_axis(2)))
    rt = int(round(joystick.get_axis(5)))
    a = axis0
    b = axis1
    c = lt
    d = rt
    pygame.event.pump()
    # Send data
    message = json.dumps({"a": a, "b": b, "c": c, "d": d})
    print(message)
    sock.send(message.encode())
