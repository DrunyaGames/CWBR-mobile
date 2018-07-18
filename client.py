from config import *
from threading import Thread
import socket
import time


class Client(Thread):

    address = ADDRESS
    buffer_size = BUFFER_SIZE

    def __init__(self):
        super().__init__()

        self.sock = None
        self.make_socket()
        self.start()

    def make_socket(self):
        try:
            self.sock = socket.create_connection(self.address)
        except ConnectionRefusedError:
            self.reconnect()

    def reconnect(self):
        print('Reconnecting in 5 second')
        self.sock.close()
        time.sleep(5)
        self.make_socket()

    def send(self, message_type, data):

        if not self.sock:
            self.make_socket()

        try:
            self.sock.sendall({'type': message_type, 'data': data})
        except ConnectionAbortedError:
            self.reconnect()

    def recv(self):
        if not self.sock:
            self.make_socket()
        try:
            temp = self.sock.recv(self.buffer_size)
            if not temp:
                raise ConnectionAbortedError
            return temp
        except ConnectionAbortedError:
            self.reconnect()
            return