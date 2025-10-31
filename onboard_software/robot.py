from autonomous import AutonomousController
from teleop import TeleopController
from client import Client
import queue
import RPi.GPIO as GPIO
from subsystems.motor_example import motor_example as motor_subsystem



class Robot:
    def __init__(self):
        self.auto_ctrl = AutonomousController()
        self.teleop_ctrl = TeleopController()
        GPIO.setmode(GPIO.BOARD)
        self.subsystem_motor = motor_subsystem()

        self.client = Client()
        self.client.start()

        data = self.client.cmd_input_queue.get()
        if data == "TELEOP START":
            self.teleop_ctrl.start()
            self.mode = "TELEOP"
        elif data == "AUTONOMOUS START":
            self.auto_ctrl.start()
            self.mode = "AUTO"


    def toggle_mode(self, data):
        if self.mode == "AUTO" and data == "SWITCH TO TELEOP":
            print("[SUPERVISOR] Switching to TELEOP")
            self.auto_ctrl.stop()
            self.teleop_ctrl.start()
            self.mode = "TELEOP"
        elif self.mode == "TELEOP" and data == "SWITCH TO AUTONOMOUS":
            print("[SUPERVISOR] Switching to AUTO")
            self.teleop_ctrl.stop()
            self.auto_ctrl.start()
            self.mode = "AUTO"

    def run(self):
        
        try:
            while True:
                try:
                    data = self.client.cmd_input_queue.get_nowait()
                except queue.Empty:
                    data = None

                self.toggle_mode(data)

                if self.mode == "AUTO":
                    cmd = data
                    telem = self.auto_ctrl.run_step(self.subsystem_motor, cmd)
                    self.client.telem_output_queue.put(telem)
                elif self.mode == "TELEOP":
                    cmd = data
                    telem = self.teleop_ctrl.run_step(cmd)
                    self.client.telem_output_queue.put(telem)

        except KeyboardInterrupt:
            print("\n[CLIENT] Interrupted by user.")
        finally:
            self.client.close()

if __name__ == "__main__":
    Robot().run()
