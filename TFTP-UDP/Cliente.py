#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys, cmd, os, time, TFTP, traceback
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import threading
import itertools


g_client = None
g_mostrar_info = False


class UDPClient:

    def __init__(self, prt, srv):
        self.puerto = prt
        self.server = srv
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.settimeout(5)
        self.chunk = 1
        self.fin_transferencia = False

    def conectar(self):
        print('Cliente conectado.')
        self.sock.connect((self.server, self.puerto))

    def desconectar(self):
        print('Cliente desconectado,')
        self.sock.close()

    def leer_archivo(self, path):
        """Transferencia del Servidor al Cliente de un archivo"""
        self.fin_transferencia = False
        paquete = TFTP.request_packet('read', path)
        print('Archivo: %s. Creado paquete RRQ: \n %s \nEnviando al servidor....\n' % (path, str(paquete)))
        self.sock.send(paquete)
        t = threading.Thread(target=self.animat)
        t.start()
        try:
            archivo = TFTP.get_filename(path)
            with open('./' + archivo, 'wb') as fo:
                while True:
                    pckt = self.sock.recv(516)
                    opcode = TFTP.tipoPaquete(pckt)

                    if opcode == '03':
                        self.sock.send(TFTP.ack_packet(TFTP.itoa(TFTP.numPaquete(pckt))))
                        recdata = TFTP.extrac_data(pckt)
                        datalength = int(len(recdata))
                        fo.write(recdata)
                        if g_mostrar_info:
                            print('Tamaño: ' + str(datalength) + ', NumPKT: ' + str(TFTP.numPaquete(pckt)))
                            print('Data: ' + repr(pckt))
                        if datalength < 512:
                            self.fin_transferencia = True
                            break

                    elif opcode == '05':
                        print('\n**ERROR ')
                        print('Codigo de paquete:' + opcode + '\nMensaje de error-> ' + TFTP.getErrMsg(pckt))
                        break

                    else:
                        print('\n*** Error desconocido en la transferencia de archivos.')
                        break

        except Exception:
            print('\n*****ERROR FATAL. Comprueba el codigo y que todo se esta ejecutando bien.')
            traceback.print_exc()

        finally:
            if opcode == '03': TFTP.comprobar_hash(path, './' + TFTP.get_filename(path))
            self.fin_transferencia = True
            self.chunk = 1

    def escribir_archivo(self, path):
        self.fin_transferencia = False
        paquete = TFTP.request_packet('write', path)
        print('Archivo: %s. Creado paquete WRQ: \n %s \nEnviando al servidor....' % (path, str(paquete)))
        self.sock.send(paquete)
        t = threading.Thread(target=self.animat)
        t.start()
        try:
            while True:
                pckt = self.sock.recv(516)
                opcode = TFTP.tipoPaquete(pckt)
                if opcode == '04':
                    path = path.replace("\\", "/")
                    with open(path, "rb") as f:
                        self.chunk = 1
                        eof = False
                        while not eof:
                            data = f.read(512)
                            eof = len(data) < 512
                            self.sock.send(TFTP.data_packet(str(self.chunk), data))
                            ack = self.sock.recv(516)
                            ack = TFTP.atoi(ack[2:])
                            if g_mostrar_info:
                                print('Recibido ACK ' + str(ack))
                            while not ack == self.chunk:
                                print('\nPackete perdido. Reenviando...')
                                self.sock.send(TFTP.data_packet(str(self.chunk), data))
                                ack = self.sock.recv(516)
                                ack = TFTP.atoi(ack[1:])
                            self.chunk += 1
                            if self.chunk > 65530:
                                print('*** Error. Limite de tamaño alcazado.')
                                break
                        f.close()
                    break
                elif opcode == '05':
                    print('\n**ERROR ')
                    print('Codigo de paquete:' + opcode + '\nMensaje de error-> ' + TFTP.getErrMsg(pckt))
                    break
                else:
                    print('\n*** Error desconocido en la transferencia de archivos.')
                    break
        except Exception:
            print('\n*****ERROR FATAL. Comprueba el codigo y que todo se esta ejecutando bien.')
            traceback.print_exc()
        finally:
            self.fin_transferencia = True
            self.chunk = 1

    def animat(self):
        self.fin_transferencia = False
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.fin_transferencia:
                break
            sys.stdout.write('\rTransfiriendo archivo ' + c)
            sys.stdout.flush()
            time.sleep(0.1)


class Comandos(cmd.Cmd):
    """Shell del cliente TCP"""
    intro = "Shell del cliente TFTP-UDP. Si necesitas ayuda, escribe '?'.\n"
    prompt = '\nTFTP@TCP>'

    def do_MOSTRAR(self, arg):
        """Imprimir por pantalla la informacion recibida por el cliente \nArgumentos: True, False"""
        try:
            opt = eval(arg)
            if isinstance(opt, bool):
                global g_mostrar_info
                g_mostrar_info = opt
                if opt:
                    print('Se mostrara la informacion de cada paqute recibido')
                else:
                    print('No se mostrara informacion de los paquetes recibidos')
        except NameError:
            print('Error en los argumentos.')

    def do_QUIT(self, arg):
        """Salir del programa """
        g_client.desconectar()
        print('Cerrando conexiones...')
        sys.exit()

    def do_INFO(self, arg):
        """Muestra informacion relevante sobre el cliente"""
        print(f'''
    Informacion sobre el cliente:
        Servidor: {g_client.server}
        Puerto: {g_client.puerto}
        Data length: {516:d}
        Modo de transferencia: {'octect'}
        Timeout: {g_client.sock.gettimeout():f} segundos
        Mostrar informacion recibida: {str(g_mostrar_info)}
            ''')

    def do_READ(self, args):
        if isinstance(args, str) and args != '':
            path = str(args)
            start_time = time.time()
            g_client.leer_archivo(path)
            elapsed_time = time.time() - start_time
            print('Tiempo : %.5f segundos' % elapsed_time)
            print('\n\n------------------ TERMINADA TRANSFERENCIA ------------------------')
        else:
            print('***Numero de argumentos invalido.')

    def do_WRITE(self, args):
        if isinstance(args, str) and args != '':
            path = args
            start_time = time.time()
            g_client.escribir_archivo(path)
            elapsed_time = time.time() - start_time
            print('Tiempo : %.5f segundos' % elapsed_time)
            print('\n\n------------------ TERMINADA TRANSFERENCIA ------------------------')

        else:
            print('***Numero de argumentos invalido.')

def init():
    """Comprobar argumentos de entrada y crear nuevo cliente"""
    server, port = None, None
    if len(sys.argv) != 5:
        print('Shell del cliente TFTP-UDP.\nNumero de argumentos insuficiente.' + '\nSaliendo...')
        time.sleep(4)
        sys.exit()
    for index, arg in enumerate(sys.argv):
        if arg == '-s':
            server = str(sys.argv[index+1])
            print('[CLIENT] Server iniciado en '+server)
        elif arg == '-p':
            port = int(sys.argv[index+1])
            print('[CLIENT] Puerto de escucha: ' + str(port))
    if server is None:
        print('Shell del cliente TFTP-UDP.\nError en el servidor.\nSaliendo...')
        time.sleep(4)
        sys.exit()
    elif port is None:
        print('Shell del cliente TFTP-UDP.\nError en el puerto.\nSaliendo...')
        time.sleep(4)
        sys.exit()
    client = UDPClient(port, server)
    return client

def main_udp():
    global g_client
    g_client = init()
    try:
        g_client.conectar()
        Comandos().cmdloop()
    except timeout:
        print('\n***Error: Timeout completado. \nVolviendo a loop\n')
        g_client.desconectar()
        main_udp()
    except Exception as ex:
        g_client.desconectar()
        print(ex)
        os._exit(1)


if __name__ == '__main__':
    main_udp()