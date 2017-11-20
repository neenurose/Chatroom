import socket
import sys
import Queue
import threading
from threading import Thread
from SocketServer import ThreadingMixIn
import re

class client(Thread):
    def __init__(self,client_socket,client_ip,client_port):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port
        self.chatroom = []
        self.chatroom_id = []
        self.client_id = 0
        self.client_name = ""
        #print("New client thread started")

    def run(self):
        '''
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

        '''
        chatroom_id_local = 0
        chatroom_local = ""


        while True:
            #print("Inside loop\n\n")
            client_message = self.client_socket.recv(2048).decode()
            #print("From client "+self.client_name+": "+client_message+"\n\n")

            client_msg_helo = client_message
            if "HELO" in client_msg_helo:
                msg_helo = client_msg_helo+"\nIP:"+host+"\nPort:"+str(port)+"\nStudentID:17312349\n"
                self.client_socket.send(msg_helo.encode())

            if "KILL_SERVICE" in client_message:
                #server_socket2.close()
                #server_socket.close()
                #print(server_socket.fileno())
                break;

            if "DISCONNECT" in client_message.split(':')[0]:
                #print(client_message)
                #thread_lock.acquire()
                #del s_queue[self.client_socket.fileno()]
                #thread_lock.release()
                disconnect_msg_1 = self.client_name+" has left this chatroom.\n\n"
                for i in self.chatroom_id:
                    disconnect_msg = "CHAT: "+str(i)+"\nCLIENT_NAME: "+self.client_name+"\n"+disconnect_msg_1
                    chatroom_members = self.getChatroomMembers(i)
                    fileno_arr = []
                    for item in chatroom_members:
                        fileno_arr.append(socket_fileno[(item,i)])

                    thread_lock.acquire()
                    #del s_queue[self.client_socket.fileno()]
                    for key in s_queue.keys():
                        #print(s_queue)
                        if key != self.client_socket.fileno() and key in fileno_arr:
                            q = s_queue[key]
                            q.put(disconnect_msg)
                    thread_lock.release()
                    #print(i)
                    self.decrementCountClientChatroom()
                    self.deassignChatroom(i)
                    self.removeFileno(i)
                    #self.client_socket.send(disconnect_msg.encode())
                self.chatroom_id = []


                self.client_socket.send(disconnect_msg.encode())
                #self.client_socket.shutdown(socket.SHUT_RDWR)
                #self.client_socket.close()
                #break;


            if "JOIN_CHATROOM" in client_message:
                client_msg_to_join = client_message
                print("\nin join",client_msg_to_join+"\n")
                client_msg_to_join_split = re.findall(r"[\w']+",client_msg_to_join)
                self.chatroom.append(client_msg_to_join_split[1])
                chatroom_local = client_msg_to_join_split[1]
                chatroom_id_local = self.getRoomId(chatroom_local);
                self.client_name = client_msg_to_join_split[7]
                self.getClientId()

                self.setFileno(chatroom_id_local)
                self.incrementCountClientChatroom()
                self.assignChatroom(chatroom_id_local)

                msg_joined = "JOINED_CHATROOM: "+chatroom_local+"\nSERVER_IP: "+host+"\nPORT: "+str(port)+"\nROOM_REF: "+str(chatroom_id_local)+"\nJOIN_ID: "+str(self.client_id)+"\n"
                print(msg_joined)
                self.client_socket.send(msg_joined.encode())

                client_joined_msg_to_chatroom = "CHAT: "+str(chatroom_id_local)+"\nCLIENT_NAME: "+self.client_name+"\nMESSAGE: "+self.client_name + " has joined this chatroom.\n"
                chatroom_members = self.getChatroomMembers(chatroom_id_local)
                print(chatroom_members)
                fileno_arr = []
                for item in chatroom_members:
                    fileno_arr.append(socket_fileno[(item,chatroom_id_local)])
                #print("\nfilenos: ",fileno_arr)
                thread_lock.acquire()
                for key in s_queue.keys():
                    if key in fileno_arr:
                        q = s_queue[key]
                        q.put(client_joined_msg_to_chatroom)
                thread_lock.release()

                for f_no in fileno_arr:
                    self.broadcast(f_no)
                #self.broadcast(self.client_socket,client_joined_msg_to_chatroom)



            if "LEAVE_CHATROOM" in client_message:
                client_msg_to_leave_split = re.findall(r"[\w']+",client_message)
                #self.chatroom.append(client_msg_to_leave_split[1])
                chatroom_id_local = client_msg_to_leave_split[1]
                chatroom_id_local = int(chatroom_id_local)
                #chatroom_id_local = self.getRoomId(chatroom_local);

                if len(s_queue.values())>1:
                    msg_to_broadcast = "CHAT: "+str(chatroom_id_local)+"\nCLIENT_NAME: "+self.client_name+"\n"+self.client_name+" has left this chatroom.\n"

                    chatroom_members = self.getChatroomMembers(chatroom_id_local)
                    fileno_arr = []
                    for item in chatroom_members:
                        fileno_arr.append(socket_fileno[(item,chatroom_id_local)])

                    thread_lock.acquire()
                    #del s_queue[self.client_socket.fileno()]
                    for key in s_queue.keys():
                        #print(s_queue)
                        if key in fileno_arr:
                            q = s_queue[key]
                            q.put(msg_to_broadcast)
                    thread_lock.release()
                    for f_no in fileno_arr:
                        self.broadcast(f_no)

                    self.decrementCountClientChatroom()
                    self.deassignChatroom(chatroom_id_local)
                    self.removeFileno(chatroom_id_local)
                    #self.client_socket.send(("From server: Broadcasted").encode())
                else:
                    self.decrementCountClientChatroom()
                    self.deassignChatroom(chatroom_id_local)
                    self.removeFileno(chatroom_id_local)
                    thread_lock.acquire()
                    #del s_queue[self.client_socket.fileno()]
                    thread_lock.release()
                self.chatroom_id.remove(chatroom_id_local)

                left_chatroom_msg = "LEFT_CHATROOM: "+str(chatroom_id_local)+"\nJOIN_ID: "+str(self.client_id)+"\n"
                self.client_socket.send(left_chatroom_msg.encode())
                #break;
                #self.client_socket.close()
                #sys.exit()
            if "CHAT" in client_message:
                #print(len(s_queue.values()))
                client_msg_to_chat_split = re.findall(r"[\w']+",client_message)

                if client_msg_to_chat_split[0] == "CHAT":
                    #self.chatroom.append(client_msg_to_chat_split[1])
                    chatroom_id_local = client_msg_to_chat_split[1]
                    chatroom_id_local = int(chatroom_id_local)
                    #chatroom_id_local = self.getRoomId(chatroom_local);
                    #msg_to_chat = client_msg_to_chat_split[7]

                    if chatroom_id_local in self.chatroom_id:
                        #print(chatroom_id_local)
                        msg_to_chat_split = client_message.split(':')
                        msg_to_chat = msg_to_chat_split[len(msg_to_chat_split)-1]
                        chat_msg = "CHAT: "+str(chatroom_id_local)+"\nCLIENT_NAME: "+self.client_name+"\nMESSAGE:"+msg_to_chat+"\n"
                        if len(s_queue.values())>1:
                            #chat_msg = "CHAT: "+str(self.chatroom_id)+"\nCLIENT_NAME: "+self.client_name+"\nMESSAGE: "+client_message+"\n\n"

                            chatroom_members = self.getChatroomMembers(chatroom_id_local)
                            #print(chatroom_members)
                            fileno_arr = []
                            for item in chatroom_members:
                                fileno_arr.append(socket_fileno[(item,chatroom_id_local)])
                            thread_lock.acquire()
                            #print("\nfilenos: ",fileno_arr)

                            for key in s_queue.keys():
                                #print(s_queue)
                                if key in fileno_arr:
                                    q = s_queue[key]
                                    q.put(chat_msg)
                            thread_lock.release()
                            self.client_socket.send((chat_msg).encode())
                            for f_no in fileno_arr:
                                self.broadcast(f_no)
                        else:
                            msg_to_send = chat_msg
                            #thread_lock.acquire()
                            #s_queue[self.client_socket.fileno()].put(msg_to_send)
                            #thread_lock.release()
                            self.client_socket.send(msg_to_send.encode())
                    else:
                        msg_to_send = "CHAT: "+str(chatroom_id_local)+"\nCLIENT_NAME: "+self.client_name+"\n"+self.client_name+" has left this chatroom.\n"
                        self.client_socket.send(msg_to_send.encode())
            #else:
                #msg_to_send = "invalid"
                #print(msg_to_send)
                #self.broadcast()
                #self.client_socket.send(msg_to_send.encode())



    def getRoomId(self,chatroom_local):
        flag = 0;
        for key in chatroom_dict:
            if key == chatroom_local.lower():
                flag = 1
                break
        if flag == 0:
            chatroom_dict[chatroom_local.lower()] = len(chatroom_dict)+1
        self.chatroom_id.append(chatroom_dict[chatroom_local.lower()])
        chatroom_id_local = chatroom_dict[chatroom_local.lower()]
        return chatroom_id_local

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

    def assignChatroom(self,chatroom_id_local):
        flag = 0
        for key in chatroom_details:
            if key == chatroom_id_local:
                chatroom_details[chatroom_id_local].append(self.client_id)
                flag = 1
        if flag == 0:
            chatroom_details[chatroom_id_local] = [self.client_id]
        #print("\nchatroom: ",chatroom_details)

    def deassignChatroom(self,chatroom_id_local):
        chatroom_details[chatroom_id_local].remove(self.client_id)
        if len(chatroom_details[chatroom_id_local]) == 0:
            del chatroom_details[chatroom_id_local]
        #print("\nchatroom: ",chatroom_details)

    def getChatroomMembers(self,chatroom_id_local):
        #print(chatroom_details)
        return chatroom_details[chatroom_id_local]

    def setFileno(self,chatroom_id_local):
        socket_fileno[(self.client_id,chatroom_id_local)] = self.client_socket.fileno()

    def removeFileno(self,chatroom_id_local):
        del socket_fileno[(self.client_id,chatroom_id_local)]

    def broadcast(self,f_no):
        for sock in socket_connections:
            if sock.fileno()==f_no:
                try:
                    msg = s_queue[sock.fileno()].get(False)
                    print(msg)
                    sock.send(msg.encode())
                except Queue.Empty:
                    pass



'''

class client_reply(Thread):
    def __init__(self,client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket;
        print("second thread")

    def run(self):
        print("hello",server_socket2)
        #server_socket2.listen(5)
        #(client_soc,(client_ip_addr, client_port_num))=server_socket2.accept()
        print("ocket2 accepted",self.client_socket.fileno())
        while True:
            try:
                msg = s_queue[self.client_socket.fileno()].get(False)
                print(msg)
                #client_soc.send(msg.encode())
                self.client_socket.send(msg.encode())
            except Queue.Empty:
                msg = "no message"
            except KeyError as e:
                pass
'''

chatroom_dict = {}
client_dict = {}
chatroom_details = {}
client_chatroom_number = {}
socket_fileno = {}
socket_connections = []


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

#server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#port2 = 5050
#server_socket2.bind(('',port2))


while True:
    print("Server is ready and listening...")
    try:
        (client_socket,(client_ip,client_port)) = server_socket.accept()
        socket_connections.append(client_socket)
    except OSError as err:
        sys.exit()
    q = Queue.Queue()
    thread_lock.acquire()

    s_queue[client_socket.fileno()] = q
    thread_lock.release()

    '''
    client_msg_helo = client_socket.recv(2048).decode()
    print(client_msg_helo)
    #for HELO message from client
    if "HELO" in client_msg_helo:
        msg_helo = client_msg_helo+"\nIP:"+host+"\nPort:"+str(port)+"\nStudentID:17312349\n"
        client_socket.send(msg_helo.encode())
    '''
    client_thread = client(client_socket,client_ip,client_port)
    client_thread.daemon = True
    client_thread.start()

    #client_thread2 = client_reply(client_socket)
    #client_thread2.daemon = True
    #client_thread2.start()
