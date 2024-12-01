import socket

# Define the host and port for the server to listen on
# Localhost, meaning the server will only be accessible from this machine
HOST = '127.0.0.1'
PORT = 4000  # Port to listen on

# Create a socket object using IPv4 addressing (AF_INET) and TCP (SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port, making the server ready to accept connections
server_socket.bind((HOST, PORT))

# Enable the server to accept connections, with a default backlog of connections
server_socket.listen()

print('Server listening on port', PORT)

# Server loop to continuously accept and handle connections
while True:
    # Accept a new connection from a client
    connection, address = server_socket.accept()
    print('Connected by', address)  # Display the client's address

    # Receive data from the client (up to 1024 bytes)
    data = connection.recv(1024)

    # If no data is received, the connection is likely closed
    if not data:
        break

    # Print the received data, decoding it from bytes to string
    print('Received Data: ', data.decode())

    # Send a response back to the client confirming receipt of the data
    connection.sendall(b'Data received successfully')

    # Close the connection with the current client
    connection.close()

# Close the server socket when done
server_socket.close()

# End of the server program
