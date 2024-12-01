import socket
import threading

# Function to receive messages


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except Exception as e:
            print(f"An error occurred while receiving message: {e}")
            client_socket.close()
            break

# Function to handle sending messages


def send_messages(client_socket):
    while True:
        message = input()
        if message.startswith("/private"):
            recipient = input("Recipient: ")
            msg = input("Message: ")
            client_socket.send(f"/private {recipient} {msg}".encode())
        elif message.startswith("/group"):
            room = input("Room name: ")
            msg = input("Message: ")
            client_socket.send(f"/group {room} {msg}".encode())
        elif message == "/logout":
            client_socket.send(message.encode())
            break

# Function to start the client


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    print("Welcome to the chat app!")
    auth_choice = input(
        "Do you want to login or signup? (login/signup): ").strip()
    client_socket.send(auth_choice.encode())

    if auth_choice == "signup":
        username = input("Choose a username: ")
        password = input("Choose a password: ")
        client_socket.send(f"{username}:{password}".encode())
    elif auth_choice == "login":
        username = input("Username: ")
        password = input("Password: ")
        client_socket.send(f"{username}:{password}".encode())

    # Receive confirmation message (Signup/Login success)
    response = client_socket.recv(1024).decode()
    print(response)

    if "successful" in response:
        # Once signup/login is successful, allow sending and receiving messages
        print("Welcome to the chat room. You can now send messages!")

        # Start a thread for receiving messages
        receive_thread = threading.Thread(
            target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Handle sending messages
        send_messages(client_socket)

    # Close the socket connection after logout
    client_socket.close()


if __name__ == "__main__":
    start_client()
