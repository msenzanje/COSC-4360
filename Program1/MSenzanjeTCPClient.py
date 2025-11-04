import socket
import sys
import os
import hashlib
import time

SERVER_PORT = 9999
BUFFER_SIZE = 4096 

def calculate_sha256(filename):
    """Calculates the SHA256 hash of a file efficiently."""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read the file in chunks and update the hash
        for byte_block in iter(lambda: f.read(BUFFER_SIZE), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Check Argument File
if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <server_ip> <filename>")
    sys.exit(1)

# Arguments from terminal
server_ip = sys.argv[1]
filename = sys.argv[2]

if not os.path.isfile(filename):
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)


client_hash = calculate_sha256(filename)
file_size_bits = os.path.getsize(filename) * 8 # IN BITS!
local_ip = socket.gethostbyname(socket.gethostname())

print(f"Attempting to connect from {local_ip} to {server_ip} on port {SERVER_PORT} ...")

# TCP Socket
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server then display info
    client_socket.connect((server_ip, SERVER_PORT))
    print(f"\nJust connected from {local_ip} to {server_ip}:{SERVER_PORT}")
    print(f"File name: {filename}")
    print(f"SHA-256: {client_hash}")
    print(f"File size: {file_size_bits} bits")

    # Send the file to the server
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
    client_socket.shutdown(socket.SHUT_WR) # After file is done, otherwise deadlock

    # Timer AFTER the file is sent
    start_time = time.time()

    # Receive the server's hash response
    server_hash = client_socket.recv(1024).decode()
    
    end_time = time.time()


    # Calculate RTT and Throughput
    rtt_ms = (end_time - start_time) * 1000
    one_way_time_s = (rtt_ms / 2) / 1000 # Half RTT in seconds

    if one_way_time_s > 0:
        # Throughput = (Size in bits) / (One-way time in seconds)
        throughput_bps = file_size_bits / one_way_time_s
        throughput_mbps = throughput_bps / 1_000_000 # Convert bits/s to Megabits/s
    else:
        throughput_mbps = float('inf') # Handle case of near-zero RTT


    print(f"RTT: {rtt_ms:.2f} ms")
    print(f"Throughput: {throughput_mbps:.2f} Mbps")

    # If hashes match
    if client_hash == server_hash:
        print("Successfully sent!")
    else:
        print("ERROR")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()