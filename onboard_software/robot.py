import server
import threading
import time

class Robot:
    def __init__(self):
        self.current_mode = None
        self.running = True

        # Initialize server
        self.server = server.Server()
        threading.Thread(target=self.server.start).start()
        while self.server.get_command() != "READY":
            time.sleep(0.1)
        print("[Robot] Startup complete!")

    def print_telemetry(self, data):
        self.server.send_telemetry(data)

    def run(self):
        num = 0

        while self.running:

            cmd = self.server.get_command()
            if cmd == "SHUTDOWN":
                self.stop()
                break

            num += 1
            if num % 50 == 0:
                self.print_telemetry({"status": num, "command": cmd})
            time.sleep(0.02)  # 50 Hz loop
    
    def stop(self):
        print("[Robot] Stopping robot")
        self.running = False
        self.server.stop()

if __name__ == "__main__":
    Robot().run()
