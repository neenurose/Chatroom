import socket
import sys
import queue
import threading
from threading import Thread
from socketserver import ThreadingMixIn
import re

class client(Thread):
    def __init__(self,client_socket,client_ip,client_port):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port
        self.chatroom = ""
        self.chatroom_id = 0
        self.client_id = 0
        self.client_name = ""
        #print("New client thread started")

    def run(self):
        client_msg_helo = self.client_socket.recv(2048).decode()
        #for HELO message from client
        if "HELO" in client_msg_helo:
            msg_helo = client_msg_helo+"\nIP:"+host+"\nPort:"+str(port)+"\nStudentID:17312349\n"
        self.client_socket.send(msg_helo.encode())

        client_msg_to_join = self.client_socket.recv(2048).decode()
        client_msg_to_join_split = re.findall(r"[\w']+",client_msg_to_join)
        self.chatroom = client_msg_to_join_split[1]
        self.getRoomId();
        self.client_name = client_msg_to_join_split[7]
        self.getClientId()

        self.setFileno()
        self.incrementCountClientChatroom()
        self.assignChatroom()

        msg_joined = "JOINED_CHATROOM: "+self.chatroom+"\nSERVER_IP: "+host+"\nPORT: "+str(port)+"\nROOM_REF: "+str(self.chatroom_id)+"\nJOIN_ID: "+str(self.client_id)
        self.client_socket.send(msg_joined.encode())

        client_joined_msg_to_chatroom = self.client_name + " joined"
        chatroom_members = self.getChatroomMembers()
        fileno_arr = []
        for item in chatroom_members:
            fileno_arr.append(socket_fileno[(item,self.chatroom_id)])
        #print("\nfilenos: ",fileno_arr)
        thread_lock.acquire()
        for key in s_queue.keys():
            if key != self.client_socket.fileno() and key in fileno_arr:
                q = s_queue[key]
                q.put(client_joined_msg_to_chatroom)
        thread_lock.release()

        while True:
            client_message = self.client_socket.recv(2048).decode()
            #print("From client "+self.client_name+": "+client_message)
            if "LEAVE_CHATROOM" in client_message:
                if len(s_queue.values())>1:
                    msg_to_broadcast = "\n"+self.client_name+" has disconnected."

                    chatroom_members = self.getChatroomMembers()
                    fileno_arr = []
                    for item in chatroom_members:
                        fileno_arr.append(socket_fileno[(item,self.chatroom_id)])

                    thread_lock.acquire()
                    del s_queue[self.client_socket.fileno()]
                    for key in s_queue.keys():
                        #print(s_queue)
                        if key != self.client_socket.fileno() and key in fileno_arr:
                            q = s_queue[key]
                            q.put(msg_to_broadcast)
                    thread_lock.release()

                    self.decrementCountClientChatroom()
                    self.deassignChatroom()
                    self.removeFileno()
                    #self.client_socket.send(("From server: Broadcasted").encode())
                else:
                    self.decrementCountClientChatroom()
                    self.deassignChatroom()
                    self.removeFileno()
                    thread_lock.acquire()
                    del s_queue[self.client_socket.fileno()]
                    thread_lock.release()

                left_chatroom_msg = "\nLEFT_CHATROOM: "+str(self.chatroom_id)+"\nJOIN_ID: "+str(self.client_id)
                self.client_socket.send(left_chatroom_msg.encode())
                break;
                #self.client_socket.close()
                #sys.exit()
            else:
                #print(len(s_queue.values()))
                chat_msg = "CHAT: "+str(self.chatroom_id)+"\nCLIENT_NAME: "+self.client_name+"\nMESSAGE: "+client_message+"\n\n"
                if len(s_queue.values())>1:
                    #chat_msg = "CHAT: "+str(self.chatroom_id)+"\nCLIENT_NAME: "+self.client_name+"\nMESSAGE: "+client_message+"\n\n"

                    chatroom_members = self.getChatroomMembers()
                    fileno_arr = []
                    for item in chatroom_members:
                        fileno_arr.append(socket_fileno[(item,self.chatroom_id)])
                    thread_lock.acquire()
                    #print("\nfilenos: ",fileno_arr)

                    for key in s_queue.keys():
                        #print(s_queue)
                        if key != self.client_socket.fileno() and key in fileno_arr:
                            q = s_queue[key]
                            q.put(chat_msg)
                    thread_lock.release()
                    self.client_socket.send((chat_msg).encode())
                else:
                    msg_to_send = chat_msg
                    #thread_lock.acquire()
                    #s_queue[self.client_socket.fileno()].put(msg_to_send)
                    #thread_lock.release()
                    self.client_socket.send(msg_to_send.encode())

    def getRoomId(self):
        flag = 0;
        for key in chatroom_dict:
            if key == self.chatroom.lower():
                flag = 1
                break
        if flag == 0:
            chatroom_dict[self.chatroom.lower()] = len(chatroom_dict)+1
        self.chatroom_id = chatroom_dict[self.chatroom.lower()]

    def getClientId(self):
        flag = 0
        for key in client_dict:
            if key == self.client_name.lower():
                flag = 1
        if flag == 0:
            client_dict[self.client_name.lower()] = len(client_dict)+1
        self.client_id = client_dict[self.client_name.lower()]

    def incrementCountClientChatroom(self):
        flag = 0
        for key in client_chatroom_number:
            if key == self.client_id:
                client_chatroom_number[self.client_id] = client_chatroom_number[self.client_id] + 1
                flag = 1
        if flag == 0:
            client_chatroom_number[self.client_id] = 1
        #print("\ncount: ",client_chatroom_number)

    def decrementCountClientChatroom(self):
        client_chatroom_number[self.client_id] = client_chatroom_number[self.client_id] - 1
        if client_chatroom_number[self.client_id] <= 0:
            del client_chatroom_number[self.client_id]
        #print("\ncount: ",client_chatroom_number)

    def assignChatroom(self):
        flag = 0
        for key in chatroom_details:
            if key == self.chatroom_id:
                chatroom_details[self.chatroom_id].append(self.client_id)
                flag = 1
        if flag == 0:
            chatroom_details[self.chatroom_id] = [self.client_id]
        #print("\nchatroom: ",chatroom_details)

    def deassignChatroom(self):
        chatroom_details[self.chatroom_id].remove(self.client_id)
        if len(chatroom_details[self.chatroom_id]) == 0:
            del chatroom_details[self.chatroom_id]
        #print("\nchatroom: ",chatroom_details)

    def getChatroomMembers(self):
        return chatroom_details[self.chatroom_id]

    def setFileno(self):
        socket_fileno[(self.client_id,self.chatroom_id)] = self.client_socket.fileno()

    def removeFileno(self):
        del socket_fileno[(self.client_id,self.chatroom_id)]



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
                #print(msg)
                client_soc.send(msg.encode())
            except queue.Empty:
                msg = "no message"
            except KeyError as e:
                pass


chatroom_dict = {}
client_dict = {}
chatroom_details = {}
client_chatroom_number = {}
socket_fileno = {}

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
