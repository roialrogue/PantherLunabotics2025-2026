import time
import random

class AutonomousController:
    def __init__(self):
        self.active = False

    def start(self):
        self.active = True
        print("[AUTO] Autonomous controller started")

    def stop(self):
        self.active = False
        print("[AUTO] Autonomous controller stopped")

    def run_step(self):
        """Run one iteration of control logic."""
        if not self.active:
            return
        print("[AUTO] Running autonomous step...")

        time.sleep(0.5)  # Simulate processing
        telem = random.sample(range(1, 101), 2)
        return telem
