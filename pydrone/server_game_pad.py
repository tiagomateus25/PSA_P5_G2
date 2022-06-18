#!/usr/bin/python3
import json
import socket
import time
import os
import pigpio

os.system("sudo pigpiod")   # Launching GPIO library
time.sleep(1)
pi = pigpio.pi()

# pins for motors-------------------------------------------------------------------------------------------------------
motor27 = 27    # left1
motor19 = 19    # left2
motor20 = 20    # right1
motor24 = 24    # right2

# motor speed-----------------------------------------------------------------------------------------------------------
throttle = 1300


def server():
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
                if axis == [-1, 0]:                             # TODO get correct values
                    throttle27 -= 100
                    throttle19 -= 100
                    throttle20 += 100
                    throttle24 += 100
                if axis == [-1, 0]:                             # TODO get correct values
                    throttle27 += 100
                    throttle19 += 100
                    throttle20 -= 100
                    throttle24 -= 100
                if axis == [-1, 0]:                             # TODO get correct values
                    throttle27 -= 100
                    throttle19 += 100
                    throttle20 += 100
                    throttle24 -= 100
                if axis == [-1, 0]:                             # TODO get correct values
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


if __name__ == "__server__":
    server()
