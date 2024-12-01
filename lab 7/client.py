import socket
import pickle
import os

# Client for interacting with the DFS


class DFSClient:
    def __init__(self, master_host='localhost', master_port=5000):
        self.master_address = (master_host, master_port)

    def upload(self, filename):
        if not os.path.exists(filename):
            print(f"File '{filename}' does not exist.")
            return

        try:
            with open(filename, 'rb') as file:
                file_data = file.read()

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(self.master_address)

            request = pickle.dumps({
                'type': 'upload',
                'filename': filename,
                'data': file_data
            })
            client_socket.send(request)

            response = client_socket.recv(1024)
            print(response.decode())
        except Exception as e:
            print(f"Error during upload: {e}")
        finally:
            client_socket.close()

    def download(self, filename):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(self.master_address)

            request = pickle.dumps({'type': 'download', 'filename': filename})
            client_socket.send(request)

            response = client_socket.recv(1024)
            response = pickle.loads(response)

            if response['status'] == 'success':
                file_data = response['data']
                with open(filename, 'wb') as file:
                    file.write(file_data)
                print(f"Downloaded and saved file: {filename}")
            else:
                print(f"Error: {response['message']}")
        except Exception as e:
            print(f"Error during download: {e}")
        finally:
            client_socket.close()


def main():
    client = DFSClient()

    while True:
        print("\nDistributed File System Client")
        print("1. Upload a file")
        print("2. Download a file")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            filename = input("Enter the filename to upload: ")
            client.upload(filename)
        elif choice == '2':
            filename = input("Enter the filename to download: ")
            client.download(filename)
        elif choice == '3':
            print("Exiting client.")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == '__main__':
    main()
