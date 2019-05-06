#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
TFTP server layered over UDP protocol
"""

import os
import sys
import time
import TFTP
from socket import socket, AF_INET, SOCK_DGRAM
from datetime import datetime
g_SERVER = None
g_PORT = None


def main():
    """Metodo principal para poner en elcucha el servidor."""
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((g_SERVER, g_PORT))
    print('Establecido en PORT:'+str(g_PORT)+', HOST:'+g_SERVER)
    while True:
        pckt, addr = sock.recvfrom(516)
        try:
            opcode = TFTP.tipoPaquete(pckt)

            if opcode == '01':
                path = TFTP.get_path(pckt)
                path = path.replace("\\", "/")
                new_print('Recibida peticion de lectura. Path: ' + path, addr)
                with open(path, "rb") as f:
                    numchunk = 1
                    eof = False
                    while not eof:
                        data = f.read(512)
                        eof = len(data) < 512
                        sock.sendto(TFTP.data_packet(str(numchunk), data), addr)
                        ack, adrr = sock.recvfrom(516)
                        ack = TFTP.atoi(ack[2:])
                        while not ack == numchunk:
                            new_print('Packete perdido. Reenviando...', addr)
                            sock.sendto(TFTP.data_packet(str(numchunk), data), addr)
                            ack, adrr = sock.recvfrom(516)
                            ack = TFTP.atoi(ack[2:])
                        numchunk = numchunk+1
                        if numchunk == 65535:
                            raise ErrorLimiteTransferencia

            elif opcode == '02':
                new_print('Recibida peticion de escritura. Path: '+TFTP.get_path(pckt), addr)
                archivo = './' + TFTP.get_filename(TFTP.get_path(pckt))
                if os.path.isfile('./' + archivo):
                    raise FileExistsError
                sock.sendto(TFTP.ack_packet(TFTP.itoa(0)), addr)
                with open(archivo, "wb") as fo:
                    eof = False
                    while not eof:
                        pckt, adrr = sock.recvfrom(516)
                        recdata = TFTP.extrac_data(pckt)
                        datalength = int(len(recdata))
                        fo.write(recdata)
                        if datalength < 512:
                            eof = True
                        sock.sendto(TFTP.ack_packet(TFTP.itoa(TFTP.numPaquete(pckt))), addr)
                        if TFTP.numPaquete(pckt) > 65535:
                            fo.close()
                            raise ErrorLimiteTransferencia
            else:
                sock.sendto(TFTP.error_packet('04', 'Operacion TFTP no encontrada.'), addr)

        except ErrorLimiteTransferencia:
            new_print('Limite de tamaño de archivo alcanzado.', addr)
            sock.sendto(TFTP.error_packet('00', 'Limite de tamaño de transferencia alcanzado.'), addr)
        except FileNotFoundError:
            sock.sendto(TFTP.error_packet('01', 'Archivo no encontrado.'), addr)
        except FileExistsError:
            new_print('El archivo solicitado ya existe en el servidor.', addr)
            sock.sendto(TFTP.error_packet('06', 'El archivo ya existe.'), addr)


class ErrorLimiteTransferencia(Exception):
    pass


def init():
    """Comprobar argumentos de entrada y crear nuevo cliente"""
    server, port = None, None
    if len(sys.argv) != 5:
        print('Shell del SERVIDOR TFTP-UDP.\nNumero de argumentos insuficiente.' + '\nSaliendo...')
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
        print('Shell del SERVIDOR TFTP-UDP.\nError en el servidor.\nSaliendo...')
        time.sleep(4)
        sys.exit()
    elif port is None:
        print('Shell del SERVIDOR TFTP-UDP.\nError en el puerto.\nSaliendo...')
        time.sleep(4)
        sys.exit()
    global g_PORT, g_SERVER
    g_PORT = port
    g_SERVER = server


def new_print(cadena, addr):
    print(datetime.today().strftime('%H:%M:%S') + ' | [' + str(addr) + '] ' + cadena)


if __name__ == "__main__":
    init()
    main()
