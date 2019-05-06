#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import time
from socketserver import DatagramRequestHandler, ForkingUDPServer


def upper(msg):
    time.sleep(1)  # simulates a more complex job
    return msg.upper()


class UpperHandler(DatagramRequestHandler):
    def handle(self):
        print('New request: {0}'.format(self.client_address))
        msg = self.rfile.read()
        self.wfile.write(upper(msg))


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

server = ForkingUDPServer(('', int(sys.argv[1])), UpperHandler)
server.serve_forever()
