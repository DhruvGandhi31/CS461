import socket
import threading
import sqlite3

# Database connection
conn = sqlite3.connect('chat.db', check_same_thread=False)
cursor = conn.cursor()

# Creating tables if they don't exist
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS messages (sender TEXT, recipient TEXT, message TEXT)''')

# Dictionary to hold online clients and groups
clients = {}
groups = {}  # Dictionary to store groups and their members

# Function to broadcast messages to all members of a group


def broadcast_group(message, room, sender=None):
    if room in groups:
        for client_socket in groups[room]:
            if client_socket != sender:
                client_socket.send(f"Group {room}: {message}".encode())

# Function to handle each client


def handle_client(client_socket, client_address):
    username = None

    # User authentication (login/signup)
    while True:
        try:
            choice = client_socket.recv(1024).decode()
            if choice == "signup":
                username, password = client_socket.recv(
                    1024).decode().split(':')
                try:
                    cursor.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    client_socket.send(
                        "Signup successful! You can now start chatting.".encode())
                except sqlite3.IntegrityError:
                    client_socket.send(
                        "Username already exists. Try a different one.".encode())
            elif choice == "login":
                username, password = client_socket.recv(
                    1024).decode().split(':')
                cursor.execute(
                    "SELECT password FROM users WHERE username=?", (username,))
                stored_password = cursor.fetchone()
                if stored_password and stored_password[0] == password:
                    client_socket.send(
                        "Login successful! Welcome to the chat.".encode())

                    # Add the user to the clients dictionary
                    clients[username] = client_socket
                    break
                else:
                    client_socket.send("Invalid credentials.".encode())
        except:
            client_socket.close()
            return

    # Handling messaging after login/signup
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if message.startswith("/private"):
                _, recipient, msg = message.split(' ', 2)
                if recipient in clients:
                    clients[recipient].send(
                        f"Private from {username}: {msg}".encode())
                    cursor.execute(
                        "INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)", (username, recipient, msg))
                    conn.commit()
                else:
                    client_socket.send("User not online.".encode())

            elif message.startswith("/group"):
                _, room, msg = message.split(' ', 2)

                if room not in groups:
                    groups[room] = []
                if client_socket not in groups[room]:
                    groups[room].append(client_socket)

                # Broadcast the message to all group members
                broadcast_group(f"{username}: {msg}",
                                room, sender=client_socket)

            elif message == "/logout":
                client_socket.send("You have logged out.".encode())
                client_socket.close()

                # Remove user from clients and groups when they logout
                if username in clients:
                    del clients[username]
                for group in groups.values():
                    if client_socket in group:
                        group.remove(client_socket)
                break
        except:
            # Handle disconnection
            client_socket.close()
            if username in clients:
                del clients[username]
            for group in groups.values():
                if client_socket in group:
                    group.remove(client_socket)
            break

# Main server function to accept incoming connections


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    start_server()
