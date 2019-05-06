#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import os
import time
import socket


class ProcessPool(object):
    def __init__(self, max_children=40):
        self.max_children = max_children
        self.children = []

    # taken from SocketServer (at Python std lib)
    def collect_children(self):
        while self.children:
            if len(self.children) < self.max_children:
                opts = os.WNOHANG
            else:
                opts = 0

            pid, status = os.waitpid(0, opts)
            if not pid:
                break

            self.children.remove(pid)

    def start_new_process(self, func, args):
        self.collect_children()
        pid = os.fork()
        if pid:
            self.children.append(pid)
        else:
            func(*args)
            sys.exit()


def upper(msg):
    time.sleep(1)  # simulates a more complex job
    return msg.upper()


def handle(sock, msg, client, n):
    print('New request: {0} {1}'.format(n, client))
    sock.sendto(upper(msg), client)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', int(sys.argv[1])))

    pool = ProcessPool()
    n = 0

    while 1:
        msg, client = sock.recvfrom(1024)
        n += 1
        pool.start_new_process(handle, (sock, msg, client, n))

if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

try:
    main()
except KeyboardInterrupt:
    pass
