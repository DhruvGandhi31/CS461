import socket
import threading


def handle_client(client_socket, client_address):
    client_ip, client_port = client_address
    print(
        f"[NEW CONNECTION] Client IP: {client_ip}, Port: {client_port} connected.")

    connected = True
    while connected:
        try:
            # Receive the initial message from the client
            message = client_socket.recv(1024).decode("utf-8")

            if message == "FILE":
                # Receive the filename
                filename = client_socket.recv(1024).decode("utf-8")
                print(f"[{client_ip}:{client_port}] Receiving file: {filename}")

                # Open a file with the received filename
                with open(f"received_{filename}", "wb") as f:
                    while True:
                        file_data = client_socket.recv(1024)
                        if not file_data:
                            break
                        f.write(file_data)

                print(f"[{client_ip}:{client_port}] File {filename} received.")
                client_socket.send(
                    f"File {filename} received successfully.".encode("utf-8"))
            else:
                print(f"[{client_ip}:{client_port}] {message}")
                client_socket.send(
                    f"Message received: {message}".encode("utf-8"))

        except Exception as e:
            print(f"Error: {e}")
            connected = False

    client_socket.close()
    print(
        f"[DISCONNECT] Client IP: {client_ip}, Port: {client_port} disconnected.")


def start_server():
    server_ip = "192.168.1.6"  # Replace with your Wi-Fi IP address
    server_port = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"[LISTENING] Server is listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()
