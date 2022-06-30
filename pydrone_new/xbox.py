#!/usr/bin/python3
import json
import socket


def xbox():
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
        connection, client_address = sock.accept()
        # xbox controllers commands
        data = connection.recv(5000)
        data = json.loads(data.decode())
        axis0 = int(data.get('a'))
        axis1 = int(data.get('b'))
        lt = int(data.get('c'))
        rt = int(data.get('d'))
        print(axis0, axis1, lt, rt)


if __name__ == "__xbox__":
    xbox()
