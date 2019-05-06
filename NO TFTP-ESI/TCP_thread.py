#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import _thread
import time
import socket


def upper(msg):
    time.sleep(1)  # simulates a more complex job
    return msg.upper()


def handle(sock, client, n):
    print('Client connected: {} {}'.format(n, client))
    while 1:
        data = sock.recv(32)
        if not data:
            break
        sock.sendall(upper(data))
    sock.close()

    print('Client disconnected: {} {}'.format(n, client))


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', int(sys.argv[1])))
sock.listen(30)

n = 0
while 1:
    child_sock, client = sock.accept()
    n += 1
    _thread.start_new_thread(handle, (child_sock, client, n))
