import socket
import threading


def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Received: {request.decode('utf-8')}")
    client_socket.send(b"ACK")
    client_socket.close()


def start_server(server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', server_port))
    server.listen(5)
    print(f"Server listening on port {server_port}")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    ports = [9998, 9999]  # List of ports for multiple servers
    for port in ports:
        server_thread = threading.Thread(target=start_server, args=(port,))
        server_thread.start()
