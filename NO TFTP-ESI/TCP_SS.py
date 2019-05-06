#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import os
import time
from socketserver import StreamRequestHandler, TCPServer


def upper(msg):
    time.sleep(1)  # simulates a more complex job
    return msg.upper()


class UpperHandler(StreamRequestHandler):
    def handle(self):
        print('Client connected: {0}'.format(self.client_address))
        while 1:
            data = os.read(self.rfile.fileno(), 32)
            if not data:
                break

            self.wfile.write(upper(data))


class customTCPServer(TCPServer):
    allow_reuse_address = True


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)


server = customTCPServer(('', int(sys.argv[1])), UpperHandler)
server.serve_forever()
