import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8080
server_socket.bind(('localhost', port))

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
