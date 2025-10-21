import time
import socket
from autonomous_controller import AutonomousController
from teleop_controller import TeleopController
from input_listener import InputListener

class Supervisor:
    def __init__(self):
        self.auto_ctrl = AutonomousController()
        self.teleop_ctrl = TeleopController()
        self.mode = "TELEOP"

        self.listener = InputListener()
        self.listener.set_callback(self.toggle_mode)
        self.listener.start()

    def toggle_mode(self):
        if self.mode == "AUTO":
            print("[SUPERVISOR] Switching to TELEOP")
            self.auto_ctrl.stop()
            self.teleop_ctrl.start()
            self.mode = "TELEOP"
        else:
            print("[SUPERVISOR] Switching to AUTO")
            self.teleop_ctrl.stop()
            self.auto_ctrl.start()
            self.mode = "AUTO"

    def run(self):

        print("[SUPERVISOR] Starting in TELEOP mode")
        self.teleop_ctrl.start()

        self.client, addr = self.server.accept()
        print("Connection accepted from " + repr(addr[1]))

        while True:
            
            self.client.send("Server approved connection\n".encode())
            print(repr(addr[1]) + ": " + self.client.recv(1026))

            if self.mode == "AUTO":
                self.auto_ctrl.run_step()
            else:
                self.teleop_ctrl.run_step()
            # You can also check for global stop condition here
            time.sleep(0.05)
        self.client.close()

            


if __name__ == "__main__":
    Supervisor().tcp_setup()
    Supervisor().run()
