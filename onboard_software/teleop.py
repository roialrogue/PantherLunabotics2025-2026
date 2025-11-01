import time
import random

'''
Axis 0 - Left Stick (L = -1, R = 1)
Axis 1 - Left Stick (T = -1, D = 1)
Axis 2 - Right Stick (L = -1, R = 1)
Axis 3 - Right Stick (T = -1, D = 1)

Axis 4 - Left Trigger (unpressed = -1, pressed = 1)
Axis 5 - Left Trigger (unpressed = -1, pressed = 1)

Button 0 - A
Button 1 - B
Button 2 - X
Button 3 - Y
Button 4 - LB
Button 5 - RB
Button 6 - Options
Button 7 - Start
'''

class TeleopController:
    def __init__(self, motor):
        self.active = False
        self.subsystem_motor = motor

    def start(self):
        self.active = True
        print("[TELEOP] Teleop control started")

    def stop(self):
        self.active = False
        print("[TELEOP] Teleop control stopped")

    def run_step(self, cmd):
        """Read joystick state and convert to control commands."""
        if not self.active:
            return
        
        x = cmd[0]
        self.subsystem_motor.set_power(x)

        telem = random.sample(range(1, 101), 6)
        
        time.sleep(0.1)
        return telem
