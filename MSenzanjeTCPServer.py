import socket
import hashlib
import os

SERVER_PORT = 9999
BUFFER_SIZE = 4096  # 4KB buffer for receiving file chunks

def calculate_sha256(filename):
    """Calculates the SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read the file in chunks and update the hash
        for byte_block in iter(lambda: f.read(BUFFER_SIZE), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))
server_socket.listen(1)
print(f"Waiting for client on port {SERVER_PORT} ...")



while True:
    # Accept a new connection
    connection_socket, addr = server_socket.accept()
    print(f"File received from {addr}")
    
    received_filename = "temp_received_file"
    try:
        # 5. Receive the file data in chunks
        with open(received_filename, "wb") as f:
            while True:
                bytes_read = connection_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)

        file_size_bits = os.path.getsize(received_filename)*8 # IN BITS!
        computed_hash = calculate_sha256(received_filename)

        print(f"File size: {file_size_bits} bits")
        print(f"SHA-256: {computed_hash}")

        # Send the computed hash back to the client
        connection_socket.sendall(computed_hash.encode())

    # Test
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        connection_socket.close()