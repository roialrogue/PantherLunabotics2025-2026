import time
import random

class AutonomousController:
    def __init__(self, motor):
        self.active = False
        self.motor = motor

    def start(self):
        self.active = True
        print("[AUTO] Autonomous controller started")

    def stop(self):
        self.active = False
        print("[AUTO] Autonomous controller stopped")

    def run_step(self, cmd):
        """Run one iteration of control logic."""
        if not self.active:
            return
        print("[AUTO] Running autonomous step...")
    

        time.sleep(0.01)  # Simulate processing
        telem = random.sample(range(1, 101), 2)
        return telem
