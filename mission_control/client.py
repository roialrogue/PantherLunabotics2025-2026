import socket
import threading
import queue
import json

class Client:
    def __init__(self, server_ip):
        self.client = socket.socket()
        port = 6767
        self.client.connect((server_ip,port))
        self.command_queue = queue.Queue()
        self.telemetry_queue = queue.Queue()

    def start(self):
        sender = threading.Thread(target=self._sender_thread, daemon=True)
        sender.start()

        receiver = threading.Thread(target=self._receiver_thread, daemon=True)
        receiver.start()

    def _sender_thread(self):

        while True:
                message = self.command_queue.get()
                self.client.sendall((json.dumps(message)+"\n").encode())

    def _receiver_thread(self):

        while True:
            with self.client.makefile('r') as stream:
                 for raw in stream:
                    raw = raw.strip()
                    if not raw:
                        continue
                    msg= json.loads(raw)
                    self.telemetry_queue.put(msg)
                    print(f"[CLIENT] Received: {self.telemetry_queue.get()}")

            data = self.client.recv(1024)  # blocking is fine here
            if data:
                self.telemetry_queue.put(data.decode())
                