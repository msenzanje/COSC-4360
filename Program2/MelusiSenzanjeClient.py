from socket import *
import time
import sys

# Create a UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)

# Server address
server_port = 9999

# Check for correct number of arguments
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <server_ip>")
    sys.exit(1)

server_ip = sys.argv[1]

# The three sentences
sentences = [
    "I'm deeply passionate about computer networking because it's the foundation of our interconnected world, enabling seamless communication, data sharing, and the backbone of the digital age.",
    "The intricacies of routing, protocols, and network security fascinate me, and I find immense joy in troubleshooting and optimizing network performance to ensure a smooth online experience for users.",
    "Studying computer networking isn't just a subject for me; it's a lifelong journey filled with endless fascination, innovation, and the thrill of mastering the technology that keeps our modern world connected."
]

try:
    for sentence in sentences:
        try:
            start_time = time.time()

            # Send ping
            client_socket.sendto(sentence.encode(), (server_ip, server_port))

            # Receive pong
            pong, server_address = client_socket.recvfrom(4096)

            end_time = time.time()
            rtt = end_time - start_time

            # Compute metrics
            length = len(sentence.encode()) * 8
            rtt_ms = rtt * 1000
            throughput_mbps = (length / rtt) / 1_000_000 if rtt > 0 else 0.0

            # Print results
            print(f"Sentence: {sentence}")
            print(f"Length: {length} bits")
            print(f"RTT: {rtt_ms:.2f} ms")
            print(f"Throughput: {throughput_mbps:.1f} Mbps\n")

        except error as err:
            print(f"Error: {err}")

finally:
    client_socket.close()