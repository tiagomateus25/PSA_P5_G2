#!/usr/bin/python3
import json
import socket
import time

# Create axis TCP/IP socket-----------------------------------------------------------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port---------------------------------------------------------------------------------------
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections-----------------------------------------------------------------------------------
sock.listen(1)

while True:
    # Wait for axis connection
    connection, client_address = sock.accept()
    try:
        while True:
            # xbox controllers commands
            data = connection.recv(5000)
            data = json.loads(data.decode())
            axis = data.get('a')
            lt = data.get('b')
            rt = data.get('c')
            print(axis, lt, rt)
            time.sleep(0.1)
    finally:
        connection.close()
