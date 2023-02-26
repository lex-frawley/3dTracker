import socket
import struct

HOST = '127.0.0.1'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    # Receive the data over the socket connection
    data = s.recv(12)  # 3 floats x 4 bytes per float

    # Convert the bytes to a tuple of floats
    tuple_of_floats = struct.unpack('fff', data)

    # Use the tuple of floats as necessary
    x, y, z = tuple_of_floats
