#!/usr/bin/env python3
import signal
from xbox360controller import Xbox360Controller
import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)


def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))


def on_button_released(button):
    print('Button {0} was released'.format(button.name))


def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    while True:
        message_axis_l = format(axis.name, axis.x)
        byt1 = message_axis_l.encode()
        sock.send(byt1)


while True:
    with Xbox360Controller(0, axis_threshold=0.2) as controller:
        # Button A events
        controller.button_trigger_l.when_pressed = on_button_pressed
        controller.button_trigger_l.when_released = on_button_released
        controller.button_trigger_r.when_pressed = on_button_pressed
        controller.button_trigger_r.when_released = on_button_released

        # Left and right axis move event
        controller.axis_l.when_moved = on_axis_moved

        signal.pause()


