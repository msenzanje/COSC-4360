from socket import *
import time
import sys

# Create a UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)

# Server address
server_port = 9999

# Check Argument File
if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <server_ip> <message>")
    sys.exit(1)

# Arguments from terminal
server_ip = sys.argv[1]
ping_message = sys.argv[2]

try:
    start_time = time.time()
    
    # Send the ping
    client_socket.sendto(ping_message.encode(), (server_ip, server_port))

    # Receive the pong (with 2048 buffer size to accommodate the long message)
    pong, server_address = client_socket.recvfrom(2048)
    
    # Calculate round-trip time
    end_time = time.time()
    rtt = end_time - start_time
    
    print(f"\nPing message sent to server")
    print(f"Pong received from server")
    print(f"Round-trip time: {rtt:.6f} seconds")

except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the socket
    client_socket.close()