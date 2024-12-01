import socket
import os


def send_message(client_socket):
    message = input("Enter message to send: ")
    client_socket.send(message.encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    print(f"Server: {response}")


def send_file(client_socket):
    file_path = input("Enter the file path to send: ")
    filename = os.path.basename(file_path)

    # Notify the server that you're sending a file
    client_socket.send("FILE".encode("utf-8"))

    # Send the file name
    client_socket.send(filename.encode("utf-8"))

    # Send the actual file content
    with open(file_path, "rb") as f:
        while (file_data := f.read(1024)):
            client_socket.send(file_data)

    print("File sent successfully.")
    response = client_socket.recv(1024).decode("utf-8")
    print(f"Server: {response}")


def start_client():
    server_ip = "192.168.1.6"  # Replace with the server Wi-Fi IP address
    server_port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    connected = True
    while connected:
        option = input(
            "Enter '1' to send a message, '2' to send a file, or 'quit' to exit: ").strip()

        if option == "1":
            send_message(client)
        elif option == "2":
            send_file(client)
        elif option.lower() == "quit":
            connected = False
        else:
            print("Invalid option, please try again.")

    client.close()


if __name__ == "__main__":
    start_client()
