from __future__ import annotations
import os
import sys
import server
import threading
import time
import teleOp
import auto
from subsystems import drivetrain
from subsystems import auger
from library import controller
import robot_params

sys.path.append(os.path.join(os.path.dirname(__file__), '../library/motor_controller/build'))
import motor_controller as mc  # type: ignore

class Robot:
    def __init__(self):
        self.current_mode = None
        self.running = True

        # Initialize global timer
        robot_params.robot_timer = robot_params.RobotTimer()

        # Initialize hardware
        self.motor_controller = mc.MotorController.get_instance("can0")
        self.drivetrain = drivetrain.Drivetrain(self.motor_controller)
        self.auger = auger.Auger(self.motor_controller)

        # Initialize server
        self.server = server.Server()
        threading.Thread(target=self.server.start).start()

        # Initialize controller and run modes
        self.controller = controller.Controller(self)
        self.teleop = teleOp.TeleOp(self)
        self.auto = auto.Auto(self)

        while self.server.get_command() != "READY":
            time.sleep(0.1)
        robot_params.robot_timer.start()
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
        self.drivetrain.stop()
        self.auger.stop()
        
if __name__ == "__main__":
    Robot().run()
