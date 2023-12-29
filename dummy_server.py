import socket
import sys

if len(sys.argv)!=2:
    print("missing arguments ; should provide IP address of server")
    exit(-1)

IP_address = sys.argv[1]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8080
server_socket.bind((IP_address, port))

server_socket.listen(5)

print(f"Server listening on port {port}...")

while True:
    client_socket, client_address = server_socket.accept()

    data = client_socket.recv(1024)
    if not data:
        break

    print(f"Received: {data.decode()}")

    client_socket.close()

server_socket.close()
