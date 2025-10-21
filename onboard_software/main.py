import time
from autonomous_controller import AutonomousController
from teleop_controller import TeleopController
from input_listener import InputListener

class Supervisor:
    def __init__(self):
        self.auto_ctrl = AutonomousController()
        self.teleop_ctrl = TeleopController()
        self.mode = "AUTO"

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
        print("[SUPERVISOR] Starting in AUTO mode")
        self.auto_ctrl.start()

        while True:
            if self.mode == "AUTO":
                self.auto_ctrl.run_step()
            else:
                self.teleop_ctrl.run_step()
            # You can also check for global stop condition here
            time.sleep(0.05)

if __name__ == "__main__":
    Supervisor().run()
