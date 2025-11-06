import socket
import queue
import json
import threading

class Server:
    def __init__(self):
        self.server = socket.socket()
        port = 6767
        self.server.bind(('',port))
        print("Socket binded to %s" %(port))

        self.server.listen(5)
        print("Socket is listening...")

        self.client, self.addr = self.server.accept()
        print("Connection accepted from " + repr(self.addr[1]))

        self.cmd_input_queue = queue.Queue()
        self.telem_output_queue = queue.Queue()



    def start(self):
        receiver = threading.Thread(target=self._receiver_thread, daemon=True)
        receiver.start()

        sender = threading.Thread(target=self._sender_thread, daemon=True)
        sender.start()

    def _sender_thread(self):
        
        while True:
            message = self.telem_output_queue.get()
            self.client.sendall((json.dumps(message)+"\n").encode())

    def _receiver_thread(self):
        stream = self.client.makefile('r')  # create once
        while True:
            raw = stream.readline()
            if not raw:
                # EOF or disconnect
                print("[SERVER] Connection closed by server.")
                break

            raw = raw.strip()
            if not raw:
                continue

            msg = json.loads(raw)
            self.cmd_input_queue.put(msg)
            print("[SERVER] Message from server:", msg)
