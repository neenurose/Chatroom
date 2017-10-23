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
                if len(s_queue.values())>1:
                    msg_to_broadcast = "From client "+str(self.client_ip)+":"+str(self.client_port)+": "+client_message
                    thread_lock.acquire()
                    del s_queue[self.client_socket.fileno()]
                    for key in s_queue.keys():
                        #print(s_queue)
                        if key != self.client_socket.fileno():
                            q = s_queue[key]
                            q.put(msg_to_broadcast)
                    thread_lock.release()
                    #self.client_socket.send(("From server: Broadcasted").encode())
                else:
                    thread_lock.acquire()
                    del s_queue[self.client_socket.fileno()]
                    thread_lock.release()

                self.client_socket.send(("Thank you for connecting").encode())
                break;
                #self.client_socket.close()
                #sys.exit()
            else:
                #print(len(s_queue.values()))
                if len(s_queue.values())>1:
                    msg_to_broadcast = "\nFrom client "+str(self.client_ip)+":"+str(self.client_port)+": "+client_message
                    thread_lock.acquire()
                    for key in s_queue.keys():
                        #print(s_queue)
                        if key != self.client_socket.fileno():
                            q = s_queue[key]
                            q.put(msg_to_broadcast)
                    thread_lock.release()
                    self.client_socket.send(("Me: "+client_message).encode())
                else:
                    msg_to_send = "Me: "+client_message
                    #thread_lock.acquire()
                    #s_queue[self.client_socket.fileno()].put(msg_to_send)
                    #thread_lock.release()
                    self.client_socket.send(msg_to_send.encode())


class client_reply(Thread):
    def __init__(self,client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket;
        #print("hello")

    def run(self):
        server_socket2.listen(1)
        (client_soc,(client_ip_addr, client_port_num))=server_socket2.accept()
        #print(self.client_socket.fileno())
        while True:
            try:
                msg = s_queue[self.client_socket.fileno()].get(False)
                print(msg)
                client_soc.send(msg.encode())
            except queue.Empty:
                msg = "no message"
            except KeyError as e:
                pass


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

server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port2 = 5050
server_socket2.bind(('',port2))


while True:
    print("Server is ready and listening...")
    (client_socket,(client_ip,client_port)) = server_socket.accept()
    q = queue.Queue()
    thread_lock.acquire()

    s_queue[client_socket.fileno()] = q
    thread_lock.release()

    client_thread = client(client_socket,client_ip,client_port)
    client_thread.daemon = True
    client_thread.start()

    client_thread2 = client_reply(client_socket)
    client_thread2.daemon = True
    client_thread2.start()
