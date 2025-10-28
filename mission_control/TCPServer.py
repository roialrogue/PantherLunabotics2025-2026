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

        self.client, self.addr = self.server.accept()
        print("Connection accepted from " + repr(self.addr[1]))

        self.message = None

    def start(self):
        t = threading.Thread(target=self._server_run, daemon=True)
        t.start()

    def _server_run(self):
        
        while True:

            if self.message != None:
                self.client.send("Server approved connection\n".encode())
                print(repr(self.addr[1]) + ": " + self.client.recv(1026))