import socket
import threading
import pickle

# Master server to manage metadata and coordinate between nodes
class MasterServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.metadata = {}  # Stores file -> node mapping
        self.nodes = {}  # Stores node info (node_id -> address)
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print("Master server started on port", self.port)
        
        while True:
            client_socket, client_address = server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
    
    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024)
            request = pickle.loads(request)
            
            if request['type'] == 'register_node':
                # Register a new data node
                node_id = request['node_id']
                node_address = request['address']
                self.nodes[node_id] = node_address
                client_socket.send(b"Node registered successfully.")
            
            elif request['type'] == 'upload':
                # Handle file upload from client
                filename = request['filename']
                file_data = request['data']
                # Distribute file to nodes (simple round-robin for now)
                node_id = list(self.nodes.keys())[0]  # Simplified: always use first node
                node_address = self.nodes[node_id]
                self.metadata[filename] = node_id
                
                # Send file to node
                self.send_file_to_node(node_address, filename, file_data)
                client_socket.send(b"File uploaded successfully.")
            
            elif request['type'] == 'download':
                # Handle file download request from client
                filename = request['filename']
                if filename in self.metadata:
                    node_id = self.metadata[filename]
                    node_address = self.nodes[node_id]
                    file_data = self.get_file_from_node(node_address, filename)
                    client_socket.send(pickle.dumps({'status': 'success', 'data': file_data}))
                else:
                    client_socket.send(pickle.dumps({'status': 'error', 'message': 'File not found.'}))
            
        except Exception as e:
            print("Error:", e)
        finally:
            client_socket.close()
    
    def send_file_to_node(self, node_address, filename, file_data):
        # Function to send file to a specific node
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.connect(node_address)
        request = pickle.dumps({'type': 'store', 'filename': filename, 'data': file_data})
        node_socket.send(request)
        node_socket.close()
    
    def get_file_from_node(self, node_address, filename):
        # Function to retrieve file from a node
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.connect(node_address)
        request = pickle.dumps({'type': 'retrieve', 'filename': filename})
        node_socket.send(request)
        response = node_socket.recv(1024)
        node_socket.close()
        return pickle.loads(response)['data']


if __name__ == '__main__':
    master_server = MasterServer()
    master_server.start()
