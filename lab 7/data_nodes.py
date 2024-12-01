import socket
import threading
import pickle
import os

# Data node that stores file chunks


class DataNode:
    def __init__(self, node_id, host='localhost', port=6000, master_host='localhost', master_port=5000):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.master_address = (master_host, master_port)
        self.storage = {}  # Dictionary to store files

    def start(self):
        # Register with the master server
        self.register_with_master()

        # Start listening for requests from master or clients
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Data node {self.node_id} started on port", self.port)

        while True:
            client_socket, client_address = server.accept()
            threading.Thread(target=self.handle_request,
                             args=(client_socket,)).start()

    def handle_request(self, client_socket):
        try:
            request = client_socket.recv(1024)
            request = pickle.loads(request)

            if request['type'] == 'store':
                # Store file data
                filename = request['filename']
                file_data = request['data']
                self.storage[filename] = file_data
                print(f"Stored file {filename}")

            elif request['type'] == 'retrieve':
                # Retrieve file data
                filename = request['filename']
                if filename in self.storage:
                    client_socket.send(pickle.dumps(
                        {'status': 'success', 'data': self.storage[filename]}))
                else:
                    client_socket.send(pickle.dumps(
                        {'status': 'error', 'message': 'File not found.'}))

        except Exception as e:
            print("Error:", e)
        finally:
            client_socket.close()

    def register_with_master(self):
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.connect(self.master_address)
        request = pickle.dumps(
            {'type': 'register_node', 'node_id': self.node_id, 'address': (self.host, self.port)})
        node_socket.send(request)
        node_socket.close()


if __name__ == '__main__':
    data_node = DataNode(node_id=1)
    data_node.start()
