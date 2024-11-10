#import socket module
from socket import *
import sys  # In order to terminate the program

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789  # You can use any available port number
serverSocket.bind(('', serverPort))  # Bind to the specified port
serverSocket.listen(1)  # Listen for incoming connections

# Get the local machine's IP address
hostname = gethostname()
server_ip = gethostbyname(hostname)

# Print the server's IP address
print(f'Server is running at IP address: {server_ip} on port {serverPort}')

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receive the request message from the client
        message = connectionSocket.recv(1024).decode()

        # Extract the filename from the message
        filename = message.split()[1]

        # Open and read the requested file
        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        # Send a new line to signify the end of the response
        connectionSocket.send("\r\n".encode())

        # Close the client socket
        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())

        # Close the client socket
        connectionSocket.close()

# Close the server socket and terminate the program
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data