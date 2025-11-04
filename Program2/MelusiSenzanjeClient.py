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

    # Receive the pong
    pong, server_address = client_socket.recvfrom(2048)
    
    end_time = time.time()
    rtt = end_time - start_time

    length = len(pong.decode()) * 8

    # Convert RTT to milliseconds
    rtt_ms = rtt * 1000
    
    # Calculate throughput in Mbps (message size in bits / RTT in seconds)
    throughput = (length / rtt) / 1000000  # Convert to Mbps
    
    
    # Display results in the required format
    print(f"Sentence: {pong.decode()}")
    print(f"Length: {length} bits")
    print(f"RTT: {rtt_ms:.2f} ms")
    print(f"Throughput: {throughput:.1f} Mbps")

except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the socket
    client_socket.close()