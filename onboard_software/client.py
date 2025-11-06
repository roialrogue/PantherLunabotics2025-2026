import socket
import queue
import json
import threading

class Client:
    def __init__(self):
        self.client = socket.socket()
        port = 6767
        self.client.connect(('',port))
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

    # def _receiver_thread(self):

    #     while True:
    #         with self.client.makefile('r') as stream:
    #             for raw in stream:
    #                 raw = raw.strip()
    #                 if not raw:
    #                     continue
    #                 msg = json.loads(raw)
    #                 self.cmd_input_queue.put(msg)
    #                 print("[CLIENT] Message from server:", msg)

    def _receiver_thread(self):
        stream = self.client.makefile('r')  # create once
        while True:
            raw = stream.readline()
            if not raw:
                # EOF or disconnect
                print("[CLIENT] Connection closed by server.")
                break

            raw = raw.strip()
            if not raw:
                continue

            msg = json.loads(raw)
            self.cmd_input_queue.put(msg)
            print("[CLIENT] Message from server:", msg)
