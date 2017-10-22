import socket
import sys

#Creating a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 2:
    print("Please provide port number")
    exit()
host = '0.0.0.0'
port = int(sys.argv[1])

server_socket.bind(('',port))
server_socket.listen(1)
print("Server is ready and listening...")

(client_socket,(client_ip,client_port)) = server_socket.accept()
client_socket.send(("Welcome to chatroom!").encode())

while True:
    client_message = client_socket.recv(2048).decode()
    print("From client: "+client_message)
    if "Bye" in client_message:
        client_socket.send(("Thank you for connecting").encode())
        server_socket.close()
        sys.exit()
    else:
        client_socket.send(("from server: "+client_message).encode())
