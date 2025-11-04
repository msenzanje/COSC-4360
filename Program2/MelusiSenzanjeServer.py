from socket import *

""" Create a UDP server """
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', 9999))

print("Waiting for client on port 9999...")

while True:
    # Receive the client packet (data) and the source address
    message, client_address = server_socket.recvfrom(2048)

    print(f'\nReceived ping from {client_address}: {message.decode()}')
    server_socket.sendto(message.decode(), client_address)