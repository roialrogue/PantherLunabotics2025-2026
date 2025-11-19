from __future__ import annotations
import server
import threading
import time
import teleOp
import auto
from dataclasses import dataclass

@dataclass
class AxisValues:
    x: float = 0.0
    y: float = 0.0
    yaw_rate: float = 0.0
    pitch_rate: float = 0.0
    lt: float = 0.0
    rt: float = 0.0

    def update(self, cmd):
        self.x = cmd[1]
        self.y = cmd[2]
        self.yaw_rate = cmd[3]
        self.pitch_rate = cmd[4]
        self.lt = cmd[5]
        self.rt = cmd[6]

    def __str__(self):
        return (f"Axis State:"
                f"  X: {self.x},"
                f"  Y: {self.y},"
                f"  Yaw Rate: {self.yaw_rate},"
                f"  Pitch Rate: {self.pitch_rate},"
                f"  Left Trigger: {self.lt},"
                f"  Right Trigger: {self.rt}")

class Controller:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.AxisValues = AxisValues()
        

    def process_axes(self, cmd):
        self.AxisValues.update(cmd)
        #print(f"[Controller] {self.AxisValues.__str__()}")

    def process_buttons(self, cmd):
        
        mode, button, action = cmd
        is_pressed = (action == "PRESSED")

        if self.robot.current_mode == "TELEOP":
            self.robot.teleop.on_button_event(button, is_pressed)
        elif self.robot.current_mode == "AUTO":
            self.robot.auto.on_button_event(button, is_pressed)

    def process_controller_inputs(self, cmd):
        if len(cmd) > 4 and cmd[0] == "TELEOP": # For now only TELEOP uses axes
            self.process_axes(cmd)
        else:
            self.process_buttons(cmd)

class Robot:
    def __init__(self):
        self.current_mode = None
        self.running = True

        # Initialize server
        self.server = server.Server()
        threading.Thread(target=self.server.start).start()

        # Initialize controller and run modes
        self.controller = Controller(self)
        self.teleop = teleOp.Teleop(self)
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

if __name__ == "__main__":
    Robot().run()
