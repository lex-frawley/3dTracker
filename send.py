import socket
import struct

class SocketSender:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        self.conn, self.addr = self.socket.accept()

    def send(self, data):
        self.conn.sendall(data)

    def close(self):
        self.conn.close()
        self.socket.close()