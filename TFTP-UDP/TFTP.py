#!/usr/bin/python3
# -*- coding: utf-8 -*-

##################################################
# generar={1 : 'read',
#        2 : 'write',
#        3 : 'data',
#        4 : 'ack',
#        5 : 'error'}
##################################################

##################################################
# Error Codes
# Value Meaning
# 0 Not defined, see error message (if any).
# 1 File not found.
# 2 Access violation.
# 3 Disk full or allocation exceeded.
# 4 Illegal TFTP operation.
# 5 Unknown transfer ID.
# 6 File already exists.
# 7 No such user.
##################################################

import struct
import ntpath
import hashlib

header_length = 4
data_length = 512
total_length = header_length + data_length


def request_packet(type, filename):
    '''   2 bytes   string    1 byte   string    1 byte
        ------------------------------------------------
        | Opcode | Filename |   0   |   Mode   |   0   |
        ------------------------------------------------
                    RRQ/WRQ packet'''

    if type == 'read':
        opcode = b'01'
    elif type == 'write':
        opcode = b'02'
    else:
        return error_packet(4, 'Illegal TFTP operation')

    mode = 'octect'
    paquete = opcode + filename.encode() + chr(0).encode() + mode.encode() + chr(0).encode()
    return paquete


def data_packet(block, data):
    '''  2 bytes    2 bytes     n bytes
        ----------------------------------
        | Opcode  |  Block #  |   Data   |
        ----------------------------------
                    DATA packet'''
    opcode = b'03'
    paquete = opcode + itoa(int(block)) + data
    return paquete


def ack_packet(block):
    '''  2 bytes    2 bytes
        ---------------------
        | Opcode |  Block # |
        ---------------------
             ACK packet'''
    opcode = b'04'
    paquete = opcode + block
    return paquete


def error_packet(errorCode, errMsg):
    '''   2 bytes    2 bytes    string   1 byte
        -----------------------------------------
        | Opcode | ErrorCode |  ErrMsg  |   0   |
        -----------------------------------------
                     ERROR packet'''
    opcode = b'05'
    paquete = opcode + errorCode.encode() + errMsg.encode() + chr(0).encode()
    return paquete


##################################################
#
#            METODOS AUXILIARES
#
##################################################

def get_path(paquete):
    '''Devuelve la ruta del archivo que esta dentro del paquete'''
    decPacket = paquete.decode('utf-8')
    decPacket = decPacket[2:-8]
    return decPacket


def get_filename(ruta):
    """Devuelve unicamente el nombre del archivo."""
    ruta, nombre = ntpath.split(ruta)
    return nombre


def extrac_data(paquete):
    return paquete[4:]


def tipoPaquete(packet):
    """Devuelve el tipo de paquete recibido"""
    opcode = packet[:2].decode('utf-8')
    return opcode


def numPaquete(packet):
    """Devuelve el numero de paquete recibido"""
    return atoi(packet[2:4])


def getErrMsg(packet):
    """Devuelve el mensaje de error contenido en el paquete"""
    packet = packet.decode('utf-8')
    errCode = packet[2:4]
    errMensaje = packet[4:-1]
    elCambioCamarero = (str(errCode) + ': ' + str(errMensaje))
    return elCambioCamarero


def itoa(numero):
    ''' Para convertir el numero a 2 bytes'''
    return struct.pack('>H', numero & 0xFFFF)


def atoi(data):
    ''' Para convertir de bytes a numero'''
    return struct.unpack('>H', data)[0]

def comprobar_hash(path_original, path_nuevo):
    hasher = hashlib.md5()
    with open(path_original, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    hasher2 = hashlib.md5()
    with open(path_nuevo, 'rb') as bfile:
        buf2 = bfile.read()
        hasher2.update(buf2)
    print(f'''
    HASH archivo origen : {hasher.hexdigest()}
    HASH archivo destino: {hasher2.hexdigest()}
    ''')
