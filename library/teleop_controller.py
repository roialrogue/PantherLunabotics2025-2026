import pygame
import time

class TeleopController:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.active = False

    def start(self):
        self.active = True
        print("[TELEOP] Teleop control started")

    def stop(self):
        self.active = False
        print("[TELEOP] Teleop control stopped")

    def run_step(self):
        """Read joystick state and convert to control commands."""
        if not self.active:
            return
        pygame.event.pump()  # Update joystick state
        x = self.joystick.get_axis(0)
        y = self.joystick.get_axis(1)
        print(f"[TELEOP] Joystick axes: x={x:.2f}, y={y:.2f}")
        time.sleep(0.1)
