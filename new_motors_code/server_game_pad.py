#!/usr/bin/python3
# socket_echo_server.py

import json
import socket
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.143.11', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(5000)
            data = json.loads(data.decode())
            a = data.get("a")
            b = data.get("b")
            c = data.get("c")
            print(a, b, c)
            time.sleep(0.1)
    finally:
        # Clean up the connection
        connection.close()
