#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import socket

sock = socket.socket()
sock.connect(('example.org', 80))

sock.send(b'''\
GET / HTTP/1.1
Host: example.org

''')

print(sock.recv(4096).decode())
