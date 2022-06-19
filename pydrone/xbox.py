#!/usr/bin/python3
import os
import pigpio
import time
import json
import socket

os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)
pi = pigpio.pi()


def xbox():

    # motors speed------------------------------------------------------------------------------------------------------
    throttle = 1500
    # pins for motors---------------------------------------------------------------------------------------------------
    motor27 = 27    # left1
    motor19 = 19    # left2
    motor20 = 20    # right1
    motor24 = 24    # right2

    # Create axis TCP/IP socket-----------------------------------------------------------------------------------------
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
            while True:
                # xbox controllers commands
                data = connection.recv(10000)
                data = json.loads(data.decode())
                axis = data.get('a')
                lt = data.get('b')
                rt = data.get('c')
                print(axis, lt, rt)

                # motors speed
                throttle27 = throttle
                throttle19 = throttle
                throttle20 = throttle
                throttle24 = throttle
                print('starting motors')
                if axis == [-1, 0]:  # go left
                    throttle27 = 1300
                    throttle19 = 1300
                    throttle20 = 1600
                    throttle24 = 1600
                if axis == [1, 0]:  # go right
                    throttle27 = 1600
                    throttle19 = 1600
                    throttle20 = 1300
                    throttle24 = 1300
                if axis == [0, -1]:  # go front
                    throttle27 = 1300
                    throttle19 = 1600
                    throttle20 = 1600
                    throttle24 = 1300
                if axis == [0, 1]:  # go back
                    throttle27 = 1600
                    throttle19 = 1300
                    throttle20 = 1300
                    throttle24 = 1600
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
                pi.set_servo_pulsewidth(motor27, throttle)
                pi.set_servo_pulsewidth(motor19, throttle)
                pi.set_servo_pulsewidth(motor20, throttle)
                pi.set_servo_pulsewidth(motor24, throttle)

        # controller()

        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__xbox__":
    xbox()
