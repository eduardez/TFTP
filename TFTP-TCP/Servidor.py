#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
TFTP server layered over TCP protocol
"""
import os
import TFTP
import sys
import time
from threading import Thread
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

g_SERVER = None
g_PORT = None


class NuevoCliente:
    def __init__(self, conexion, socke, addres):
        self.conn = conexion
        self.sock = socke
        self.addr = addres

    def main_loop(self):
        new_print('Nueva conexion establecida.', self.addr)
        while True:
            try:
                pckt = self.conn.recv(516)
                opcode = TFTP.tipoPaquete(pckt)

                if opcode == '01':
                    new_print('Peticion de lectura: %s' % TFTP.get_path(pckt), self.addr)
                    path = TFTP.get_path(pckt)
                    path = path.replace("\\", "/")
                    with open(path, "rb") as f:
                        num_chunk = 1
                        eof = False
                        while not eof:
                            data = f.read(512)
                            eof = len(data) < 512
                            self.conn.send(TFTP.data_packet(str(num_chunk), data))
                            num_chunk = num_chunk + 1

                elif opcode == '02':
                    new_print('Peticion de escritura: %s' % TFTP.get_path(pckt), self.addr)
                    archivo = TFTP.get_filename(TFTP.get_path(pckt))
                    if os.path.isfile('./'+archivo):
                        raise FileExistsError
                    self.conn.send(TFTP.ack_packet(TFTP.itoa(1)))
                    with open('./' + archivo, "wb") as fo:
                        eof = False
                        while not eof:
                            pckt = self.conn.recv(516)
                            recdata = TFTP.extrac_data(pckt)
                            data_length = int(len(recdata))
                            fo.write(recdata)
                            if data_length < 512:
                                eof = True

                elif opcode == '06':
                    new_print('Cliente desconectado.', str(self.addr))
                    self.conn.close()
                    break

                else:
                    self.conn.send(TFTP.error_packet('04', 'Operacion TFTP no encontrada.'))
                    break

            except FileNotFoundError:
                new_print('El archivo solicitado no se ha podido encontrar.', self.addr)
                self.conn.send(TFTP.error_packet('01', 'Archivo no encontrado.'))
            except FileExistsError:
                new_print('El archivo solicitado ya existe en el servidor.', self.addr)
                self.conn.send(TFTP.error_packet('06', 'El archivo ya existe.'))


def new_print(cadena, addr):
    print(datetime.today().strftime('%H:%M:%S') + ' | [' + str(addr) + '] ' + cadena)


def init():
    """Comprobar argumentos de entrada y crear nuevo cliente"""
    server, port = None, None
    if len(sys.argv) != 5:
        print('Shell del SERVIDOR TFTP-TCP.\nNumero de argumentos insuficiente.' + '\nSaliendo...')
        time.sleep(4)
        sys.exit()
    for index, arg in enumerate(sys.argv):
        if arg == '-s':
            server = str(sys.argv[index+1])
            print('[SERVER] Server iniciado en '+server)
        elif arg == '-p':
            port = int(sys.argv[index+1])
            print('[SERVER] Puerto de escucha: ' + str(port))
    if server is None:
        print('Shell del SERVIDOR TFTP-TCP.\nError en el servidor.\nSaliendo...')
        time.sleep(4)
        sys.exit()
    elif port is None:
        print('Shell del SERVIDOR TFTP-TCP.\nError en el puerto.\nSaliendo...')
        time.sleep(4)
        sys.exit()
    global g_PORT, g_SERVER
    g_PORT = port
    g_SERVER = server


def main():
    sock = socket(AF_INET,SOCK_STREAM)
    sock.bind((g_SERVER,g_PORT))
    print('Establecido en PORT:'+str(g_PORT)+', HOST:'+g_SERVER)
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        nuevo = NuevoCliente(conn, sock, addr)
        Thread(target=nuevo.main_loop).start()


if __name__ == "__main__":
    init()
    main()