from onboard_software.autonomous import AutonomousController
from onboard_software.teleop import TeleopController
from onboard_software.server import Server
import queue
import RPi.GPIO as GPIO
from onboard_software.subsystems.motor_example import MotorExample
        
class Robot:
    def __init__(self):
        self.robot = RobotCore()
        self.auto_ctrl = AutonomousController(self.robot)
        self.teleop_ctrl = TeleopController(self.robot)

        self.server = Server()
        self.server.start()

        data = self.server.cmd_input_queue.get()
        if data[0] == "TELEOP START":
            self.teleop_ctrl.start()
            self.mode = "TELEOP"
        elif data[0] == "AUTONOMOUS START":
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
        id = self.mode # startup mode initialisation
        try:
            while True:
                try:
                    data = self.server.cmd_input_queue.get_nowait()
                    id = data[0]
                    print(id)
                    if id.startswith("SWITCH"):
                         self.toggle_mode(id)

      
                except queue.Empty:
                    data = None

                cmd = data
                print(self.mode)
                if self.mode == "AUTO" and id == "AUTO":
                    telem = self.auto_ctrl.run_step(cmd)
                    self.server.telem_output_queue.put(telem)
                elif self.mode == "TELEOP" and id == "TELEOP":
                    telem = self.teleop_ctrl.run_step(cmd)
                    self.server.telem_output_queue.put(telem)

        except KeyboardInterrupt:
            print("\n[CLIENT] Interrupted by user.")
        finally:
            # self.server.close()
            self.robot.stop()

class RobotCore:
    def __init__(self):
        # Contains all subsystems and initializes GPIO
        GPIO.setmode(GPIO.BOARD)
        self.subsystem_motor = MotorExample()

    def stop(self):
        GPIO.cleanup()
        self.subsystem_motor.stop()
        

if __name__ == "__main__":
    Robot().run()
