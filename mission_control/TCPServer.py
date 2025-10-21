import socket
import threading

class Server:
    def __init__(self):
        self.server = socket.socket()
        port = 6767
        self.server.bind(('192.168.1.10',port))
        print("Socket binded to %s" %(port))

        self.server.listen(5)
        print("Socket is listening...")