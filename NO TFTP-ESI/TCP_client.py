#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <host> <port>"

import sys
import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1], int(sys.argv[2])))

    while 1:
        data = sys.stdin.readline().strip().encode()
        if not data:
            break

        sent = sock.send(data)

        msg = bytes()
        while len(msg) < sent:
            msg += sock.recv(32)

        print("Reply is '{0}'".format(msg.decode()))

    sock.close()

if len(sys.argv) != 3:
    print(__doc__.format(__file__))
    sys.exit(1)

try:
    main()
except KeyboardInterrupt:
    pass
