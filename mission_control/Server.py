import socket
import threading
import queue

class Server:
    def __init__(self):
        self.server = socket.socket()
        port = 6767
        self.server.bind(('10.154.8.96',port))
        print("Socket binded to %s" %(port))

        self.server.listen(5)
        print("Socket is listening...")

        self.client, self.addr = self.server.accept()
        print("Connection accepted from " + repr(self.addr[1]))

        self.command_queue = queue.Queue()
        self.telemetry_queue = queue.Queue()

    def start(self):
        sender = threading.Thread(target=self._sender_thread, daemon=True)
        sender.start()

        receiver = threading.Thread(target=self._receiver_thread, daemon=True)
        receiver.start()

    def _sender_thread(self):
        print(f"[SERVER] Connected sender thread to {self.addr[1]}")

        while True:
                message = self.command_queue.get()
                self.client.send(message.encode())
                print(f"[SERVER] Sent: {message}")


    def _receiver_thread(self):
        print(f"[SERVER] Connected receiver thread to {self.addr[1]}")

        while True:
            data = self.client.recv(1024)  # blocking is fine here
            if data:
                self.telemetry_queue.put(data.decode())
                print(f"[SERVER] Received: {data.decode()}")