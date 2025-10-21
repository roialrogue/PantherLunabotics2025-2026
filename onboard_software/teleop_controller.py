import pygame
import time

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
        pygame.event.pump()                  # Update joystick state
        x = self.joystick.get_axis(0)        # forward and reverse (Left Stick up and down)
        y = self.joystick.get_axis(1)        # strafe left and right (Left Stick left and right)
        yaw_rate = self.joystick.get_axis(2) # yaw angle rate (Right Stick left and right)
        start_mining_motor = self.joystick.get_button(4) # start mining belt motor (LB)
        stop_mining_motor = self.joystick.get_button(5)  # stop mining belt motor (RB)
        start_dumping_motor = self.joystick.get_axis(4)  # start mining belt motor (LT)
        stop_dumping_motor = self.joystick.get_axis(5)   # stop mining belt motor (RT)
        
        
        print(f"[TELEOP] Joystick axes: x={x:.2f}, y={y:.2f}")
        time.sleep(0.1)
