#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import time
import socket
import signal


def upper(msg):
    time.sleep(1)  # simulates a more complex job
    return msg.upper()


def handle(sock, client):
    print('Client connected: {0}'.format(client))
    while 1:
        data = sock.recv(32)
        if not data:
            break

        sock.sendall(upper(data))

    sock.close()
    print('Client disconnected: {0}'.format(client))


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

signal.signal(signal.SIGINT, lambda n, f: sys.exit(0))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', int(sys.argv[1])))
sock.listen(30)

while 1:
    child_sock, client = sock.accept()
    handle(child_sock, client)
