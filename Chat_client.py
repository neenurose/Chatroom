import socket
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Please provide IP address and port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
client_socket.connect((IP_address, Port))

while True:
    message_server = client_socket.recv(2048).decode()
    if "Thank you" in message_server:
        print(message_server)
        client_socket.close()
        sys.exit()
    else:
        if len(message_server)>0:
            print(message_server)

        sys.stdout.write("Type a Message: ")
        sys.stdout.flush()
        message_client = sys.stdin.readline()
        client_socket.send(message_client.encode())
