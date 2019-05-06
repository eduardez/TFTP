#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Eduardez


from time import sleep
import os
import urllib3, urllib.request, json

g_DirName='/gatetes'
g_DirActual=os.getcwd()

def crearDir():
    ruta=g_DirActual+g_DirName
    print('Creando directorio ' + ruta)
    try:  
        if(os.path.isdir(ruta)):
            #print("El directorio ya existe")
            pass
        else:
            os.mkdir(ruta)
    except OSError:  
        print ("La creacion de %s fallo baby" % ruta)
        
def borrarTmp():
    print('Limpiando archivos temporales... ')
    ruta=g_DirActual+g_DirName
    try:  
        os.rmdir(ruta)
    except OSError:  
        print ('Error borrando el directorio temporal')
        
def coger(num):
    ruta=g_DirActual+g_DirName
    with urllib.request.urlopen("https://api.thecatapi.com/v1/images/search") as url:
        data = str(json.loads(url.read().decode()))
    data=data.split(',')
    posURL=0
    for x in range(0,len(data)-1):
        if 'url' in data[x]:
            posURL=x

    urlPIC=str(data[posURL]).split(': ')
    urlPIC=urlPIC[1]
    urlPIC=urlPIC[1:-1]
    print(urlPIC)
    extension=str(urlPIC).split('.')
    extension=extension[len(extension)-1]

    opener = urllib.request.build_opener()    
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(urlPIC, ruta+'/Gatoto_'+str(num)+'.'+str(extension))

def generarImagen(num):
    crearDir()
    coger(num)
    pass


if __name__ == '__main__':
    salida = 0
    while(not salida):
        print("""
------------------------------------------------
        Generador aleatorio de gatetes

1.DAME MIS GATOS YA
0.Salir
        """)
        opcion=int(input("Opcion: "))
        if(opcion==1):
            veces=(int(input('Numero de gatetes a conseguir: ')))
            for x in range(0,veces):
                generarImagen(x)
            print('Todos los gatetes han sido descargados.')
        elif(opcion==0):    
            borrarTmp()
            print("Adios mesie")
            salida=1;
        else:
            print("Opcion no encontrada.")
            sleep(0.5)
            
            
                
        