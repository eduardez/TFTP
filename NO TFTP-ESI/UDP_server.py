#!/usr/bin/python3 -u
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import time
import socket


def upper(msg):
    time.sleep(1)  # simulates a more complex job
    return msg.upper()


def handle(sock, msg, client, n):
    print("New request {0} {1}".format(n, client))
    sock.sendto(upper(msg), client)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ('', int(sys.argv[1]))
    sock.bind(address)

    n = 0
    while 1:
        msg, client = sock.recvfrom(1024)
        n += 1
        handle(sock, msg, client, n)


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

try:
    main()
except KeyboardInterrupt:
    pass
