import socket
import threading
import json
import queue
import time

# Laptop Client robot controller
class Client:
    def __init__(self, server_ip):
        self.host = server_ip
        self.port = 6767
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.input_queue = queue.Queue() # For incoming telemetry and ACKs
        self.output_queue = queue.Queue() # For outgoing commands and ACKs
        self.running = True
        self.message_id = 0
        self.pending_acks = {}
        self.ack_timeout = 1 # seconds

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print("[Client (Laptop)] Connected to server at : " + self.host)

        threading.Thread(target=self._sender_thread).start()
        threading.Thread(target=self._receiver_thread).start()
        threading.Thread(target=self._ack_monitor_thread).start()

        # Process incoming telemetry and ACKs
        while self.running:
            try:
                msg = self.input_queue.get(timeout=5)  # Wait up to 5 second for a message
                if msg.get('type') == 'telemetry':
                    #self.controller.handle_telemetry(msg)  # TODO: Process telemetry
                    print(f"[Client (Laptop)] Telemetry received: {msg}")
                    # Send ACK for telemetry
                    ack = {"type": "ack", "id": msg.get('id')}
                    self.output_queue.put(ack)
                elif msg.get('type') == 'ack':
                    # Handle ACK: Remove from pending
                    msg_id = msg.get('id')
                    if msg_id in self.pending_acks: 
                        del self.pending_acks[msg_id]
                        print(f"[Client (Laptop)] ACK received for message ID {msg_id}")
            except queue.Empty:
                continue


    def _receiver_thread(self):
        stream = self.client_socket.makefile('r')  # Create a file-like object
        try:
            while self.running:
                raw = stream.readline()  # Read a line from the stream
                if not raw:  # If no data is read (connection closed)
                    print("[Client (Laptop)] Connection closed by robot server.")
                    self.running = False
                    break
                raw = raw.strip()  # Remove leading/trailing whitespace
                if not raw:  # If the stripped string is empty
                    continue
                msg = json.loads(raw)  # Parse the string as JSON
                self.input_queue.put(msg)
                print(f"[Client (Laptop)] Received: {msg}")
        finally:
            stream.close()

    def send_command(self, data):
        msg = {"type": "command", "id": self.message_id, "data": data}
        self.output_queue.put(msg)
        self.pending_acks[self.message_id] = (msg, time.time())
        self.message_id += 1
        
    def _sender_thread(self):
        stream = self.client_socket.makefile('w')  # Create a file-like object
        try:
            while self.running:
                try:
                    msg = self.output_queue.get(timeout=1)  # Wait up to 1 second for a message
                    json_str = json.dumps(msg) + '\n'  # Convert the message to JSON string
                    stream.write(json_str)  # Write the JSON string to the stream
                    stream.flush()  # Flush the stream to ensure data is sent immediately
                    print(f"[Client (Laptop)] Sent: {msg}")
                except queue.Empty:
                    continue
        finally:
            stream.close()

    def _ack_monitor_thread(self):
        while self.running:
            current_time = time.time()
            to_resend = []
            for msg_id, (msg, sent_time) in self.pending_acks.items():
                if current_time - sent_time > self.ack_timeout:
                    to_resend.append(msg)
            for msg in to_resend:
                print(f"[Client (Laptop)] Resending unacknowledged message: {msg}")
                self.output_queue.put(msg)
                self.pending_acks[msg['id']] = (msg, time.time())  # Update the timestamp in pending ACKs
            time.sleep(0.2)  # Check every 0.2 seconds

    def stop(self):
        self.running = False
        self.client_socket.close()
                