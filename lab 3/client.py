import socket
import threading


def send_message(server_ip, server_port, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    client.send(message.encode('utf-8'))
    response = client.recv(4096)
    print(f"Received: {response.decode('utf-8')}")
    client.close()


if __name__ == "__main__":
    server_ip = '127.0.0.1'
    ports = [9998, 9999]  # List of server ports
    messages = ["Hello Server 1", "Hello Server 2"]

    for port, message in zip(ports, messages):
        client_thread = threading.Thread(
            target=send_message, args=(server_ip, port, message))
        client_thread.start()
