import socket

# Define the host and port to connect to the server
# The server's hostname or IP address (localhost in this case)
HOST = '127.0.0.1'
PORT = 4000  # The port used by the server

# Create a socket object using IPv4 addressing (AF_INET) and TCP (SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the specified server and port
client_socket.connect((HOST, PORT))

# Prompt the user to enter a message to send to the server
message = input('Enter a message: ')

# Send the user's message to the server, encoding it into bytes
client_socket.sendall(message.encode())

# Wait to receive a response from the server (up to 1024 bytes)
data = client_socket.recv(1024)

# Print the server's response, decoding it from bytes to string
print('Received: ', data.decode())

# Close the connection to the server
client_socket.close()
