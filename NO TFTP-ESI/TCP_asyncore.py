#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import asyncore
import time
import socket


def upper(msg):
    time.sleep(1)  # simulates a more complex job
    return msg.upper()


class ChildHandler(asyncore.dispatcher):
    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock)
        self.data = bytes()

    def handle_read(self):
        self.data += upper(self.recv(32))

    def writable(self):
        return (len(self.data) > 0)

    def handle_write(self):
        sent = self.send(self.data.upper())
        self.data = self.data[sent:]

    def handle_close(self):
        self.close()


class ParentHandler(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', int(sys.argv[1])))
        self.listen(30)

    def handle_accept(self):
        child_sock, client = self.accept()
        print('Client connected: {}'.format(client))
        ChildHandler(child_sock)


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

ParentHandler()
asyncore.loop()
