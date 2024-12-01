import socket
import threading


class Server:
    def __init__(self, host='127.0.0.1', port=9000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = {}

        print(f"Server running on {host}:{port}")

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                packet = client_socket.recv(1024).decode()
                if not packet:
                    break

                # Registration
                if packet.startswith('id_'):
                    client_id = packet[3:]
                    self.clients[client_id] = 0
                    print(f"Registered client ID: {client_id}")

                # Withdrawal
                elif packet.startswith('1'):
                    id, amount = packet[1:].split('.')
                    amount = int(amount)
                    if self.clients.get(id, 0) < amount:
                        # Insufficient funds
                        client_socket.sendall("0".encode())
                    else:
                        self.clients[id] -= amount
                        client_socket.sendall("1".encode())  # Successful

                # Deposit
                elif packet.startswith('2'):
                    id, amount = packet[1:].split('.')
                    amount = int(amount)
                    self.clients[id] = self.clients.get(id, 0) + amount
                    client_socket.sendall("1".encode())  # Successful

                # Transfer
                elif packet.startswith('3'):
                    id, id2, amount = packet[1:].split('.')
                    amount = int(amount)
                    if self.clients.get(id, 0) < amount:
                        # Insufficient funds
                        client_socket.sendall("0".encode())
                    elif id2 not in self.clients:
                        # Invalid recipient
                        client_socket.sendall("1".encode())
                    else:
                        self.clients[id] -= amount
                        self.clients[id2] += amount
                        client_socket.sendall("2".encode())  # Successful

                # Balance inquiry
                elif packet.startswith('4'):
                    balance = self.clients.get(packet[1:], 0)
                    client_socket.sendall(str(balance).encode())

                # Exit
                elif packet.startswith('5'):
                    print(f"Client {client_address} disconnected.")
                    break
        finally:
            client_socket.close()

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection established with {client_address}")
            threading.Thread(target=self.handle_client, args=(
                client_socket, client_address)).start()


if __name__ == "__main__":
    server = Server()
    server.start()
