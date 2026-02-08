from __future__ import annotations
import os
import sys
import server
import threading
import time
import teleOp
import auto
from library.Controller import Controller

sys.path.append(os.path.join(os.path.dirname(__file__), '../../library/motor_controller/build'))
try:
    import motor_controller as mc
except ImportError as e:
    print(f"ERROR: Failed to import motor_controller module: {e}")
    print("Make sure the module is compiled and the path is correct")
    sys.exit(1)


class Robot:
    def __init__(self):
        self.current_mode = None
        self.running = True

        # Initialize hardware
        self.core = RobotCore()
        self.core.intializeHardware()

        # Initialize server
        self.server = server.Server()
        threading.Thread(target=self.server.start).start()

        # Initialize controller and run modes
        self.controller = Controller(self)
        self.teleop = teleOp.TeleOp(self)
        self.auto = auto.Auto(self)

        while self.server.get_command() != "READY":
            time.sleep(0.1)
        print("[Robot] Startup complete!")

    def print_telemetry(self, data):
        self.server.send_telemetry(data)

    def run(self):

        while self.running:

            cmd = self.server.get_command()
            if cmd == "SHUTDOWN":
                self.stop()
                break

            if cmd is not None:
                self.current_mode = cmd[0]
                self.controller.process_controller_inputs(cmd)

            if self.current_mode == "TELEOP":
                self.teleop.run_teleOp_step()
            elif self.current_mode == "AUTO":
                self.auto.run_auto_step()
    
    def stop(self):
        print("[Robot] Stopping robot")
        self.running = False
        self.server.stop()

class RobotCore:
    def intializeHardware(self):
        print("[RobotCore] Initializing hardware")
        self.motor_controller = mc.MotorController().getInstance("can0")
        
if __name__ == "__main__":
    Robot().run()