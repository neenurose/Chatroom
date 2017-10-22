import socket
import sys
import queue
import threading
from threading import Thread
from socketserver import ThreadingMixIn

class client(Thread):
    def __init__(self,client_socket,client_ip,client_port):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port
        print("New client thread started")

    def run(self):
        self.client_socket.send(("Welcome to chatroom!").encode())
        while True:
            client_message = self.client_socket.recv(2048).decode()
            print("From client "+str(self.client_ip)+":"+str(self.client_port)+": "+client_message)
            if "Bye" in client_message:
                self.client_socket.send(("Thank you for connecting").encode())
                break;
                #self.client_socket.close()
                #sys.exit()
            else:
                self.client_socket.send(("from server: "+client_message).encode())


thread_lock = threading.Lock()
s_queue = {}
#Creating a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 2:
    print("Please provide port number")
    exit()
host = '0.0.0.0'
port = int(sys.argv[1])

server_socket.bind(('',port))
server_socket.listen(5)

while True:
    print("Server is ready and listening...")
    (client_socket,(client_ip,client_port)) = server_socket.accept()
    q = queue.Queue()
    thread_lock.acquire()

    s_queue[client_socket.fileno()] = queue
    thread_lock.release()

    newthread = client(client_socket,client_ip,client_port)
    newthread.daemon = True
    newthread.start()
