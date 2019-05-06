#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import cmd
import traceback
import time
import TFTP
import threading
from socket import socket, AF_INET, SOCK_STREAM, timeout


g_client = None
g_mostrar_info = False

'''Cliente TFTP sobre TCP'''


class ClaseCliente:
    """
    Clase Cliente.

    """
    def __init__(self, prt, srvr):
        self.puerto = prt
        self.server = srvr
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.settimeout(5)
        self.chunk = 1
        self.fin_transferencia = False
        self.limite_integer = 0

    """Metodo usado para desconectar el Cliente del Servidor. 
    Ya que es TCP, se envia un tipo de paquete no indicado 
    en la docu de TFTP (ID: 06)
    """
    def desconectar(self):
        self.fin_transferencia = True
        self.sock.send(TFTP.quit_packet())
        print('Cliente desconectado.')

    """Metodo usado para establecer la conexion entre el Cliente y el Servidor."""
    def conectar(self):
        self.sock.connect((self.server, self.puerto))
        print('Cliente conectado.')

    """Metodo para leer un archivo el cual se almacenara en la carpeta del Cliente. 
    Este archivo se guardara con el mismo nombre del archivo de origen. Si hay un archivo con
    el mismo nombre, se sobreescribira.
    opcode : str
        Codigo de operacion del paquete recibido
    chunk : int
        Numero de chunks leidos
    """
    def leer_archivo(self, path):
        self.fin_transferencia = False
        paquete = TFTP.request_packet('read', path)
        print('\nArchivo: %s. Creado paquete RRQ: \n%s \nEnviando al servidor....\n' % (TFTP.get_filename(path), str(paquete)))
        self.sock.send(paquete)
        t = threading.Thread(target=self.animate)
        t.start()
        try:
            global g_mostrar_info
            archivo = TFTP.get_filename(path)
            with open('./' + archivo, 'wb') as fo:
                while True:
                    pckt = self.sock.recv(516)
                    opcode = TFTP.tipoPaquete(pckt)

                    if opcode == '03':
                        rec_data = TFTP.extrac_data(pckt)
                        fo.write(rec_data)
                        data_length = int(len(rec_data))
                        self.chunk = TFTP.numPaquete(pckt)
                        if self.chunk == 65535: self.limite_integer += 1
                        if g_mostrar_info:
                            print('Tamaño: ' + str(data_length) + ', NumPKT: ' + str(self.chunk))
                            print('Data: ' + repr(pckt))
                        if data_length < 512:
                            self.fin_transferencia = True
                            break

                    elif opcode == '05':
                        print('**ERROR ')
                        print('Codigo de paquete:' + opcode + '\nMensaje de error-> ' + TFTP.getErrMsg(pckt))
                        break

                    else:
                        print('*** Error desconocido en la transferencia de archivos.')
                        break
        except Exception:
            print('\n*****ERROR FATAL. Comprueba el codigo del CLIENTE (RRQ).')
            traceback.print_exc()

        finally:
            if opcode == '03':TFTP.comprobar_hash(path, './' + TFTP.get_filename(path))
            self.fin_transferencia = True
            self.chunk = 1

    """Metodo para excribir un archivo el cual se almacenara en la carpeta del Servidor. 
      Este archivo se guardara con el mismo nombre del archivo de origen. Si hay un archivo con
      el mismo nombre, NO se sobreescribira.
      opcode : str
        Codigo de operacion del paquete recibido
      chunk : int
        Numero de chunks leidos
      """
    def escribir_archivo(self, path):
        self.fin_transferencia = False
        paquete = TFTP.request_packet('write', path)
        print('\nArchivo: %s. Creado paquete WRQ: \n%s \nEnviando al servidor....' % (TFTP.get_filename(path), str(paquete)))
        self.sock.send(paquete)
        t = threading.Thread(target=self.animate)
        t.start()
        try:
            while True:
                pckt = self.sock.recv(516)
                opcode = TFTP.tipoPaquete(pckt)

                if opcode == '04':
                    path = path.replace("\\", "/")
                    print('Filename: ' + path)
                    with open(path, "rb") as f:
                        self.chunk = 1
                        eof = False
                        while not eof:
                            data = f.read(512)
                            eof = len(data) < 512
                            self.sock.send(TFTP.data_packet(str(self.chunk), data))
                            if g_mostrar_info:
                                print(repr(data), end='')
                            self.chunk += 1
                        f.close()
                    self.fin_transferencia = True
                    break

                elif opcode == '05':
                    print('\n**ERROR. Codigo de paquete:' + opcode + '\nMensaje de error-> ' + TFTP.getErrMsg(pckt))
                    break

                else:
                    print('\n*** Error desconocido en la transferencia de archivos.')
                    print('\nPaquete:' + str(pckt))

                    break
        except Exception:
            print('\n*****ERROR FATAL. Comprueba el codigo del CLIENTE (WRQ).')
            traceback.print_exc()
        finally:
            self.fin_transferencia = True
            self.chunk = 1

    """Animacion para comprobar que la transferencia no se atasque."""
    def animate(self):
        self.limite_integer = 0
        while not self.fin_transferencia:
            mbyt = ((self.chunk + (65535 * self.limite_integer))*512)/(1024*1024)
            sys.stdout.write('\rTransferido: %.2f MBytes' % (mbyt))
            sys.stdout.flush()
            time.sleep(0.2)
            if self.fin_transferencia:
                break


class Comandos(cmd.Cmd):
    """Shell del cliente TCP"""
    intro = "Shell del cliente TFTP-TCP. Si necesitas ayuda, escribe '?'.\n"
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
        print('''
Informacion sobre el cliente:
    Servidor: %s
    Puerto: %s
    Data length: %d
    Modo de transferencia: %s
    Timeout: %f segundos
    Mostrar informacion recibida: %s
        ''' % (g_client.server, g_client.puerto, 516, 'octect', g_client.sock.gettimeout(), str(g_mostrar_info)))

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
        print('Shell del cliente TFTP-TCP.\nNumero de argumentos insuficiente.' + '\nSaliendo...')
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
        print('Shell del cliente TFTP-TCP.\nError en el servidor.\nSaliendo...')
        time.sleep(4)
        sys.exit()
    elif port is None:
        print('Shell del cliente TFTP-TCP.\nError en el puerto.\nSaliendo...')
        time.sleep(4)
        sys.exit()
    client = ClaseCliente(port, server)
    return client


def main_tcp():
    global g_client
    g_client = init()
    try: 
        g_client.conectar()
        Comandos().cmdloop()
    except timeout:
        print('\n***Error: Timeout completado. \nVolviendo a loop\n')
        g_client.desconectar()
        main_tcp()
    except Exception as ex:
        g_client.desconectar()
        print(ex)


if __name__ == '__main__':  
    main_tcp()
