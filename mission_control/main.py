import time
import pygame
from server import Server

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

class Supervisor:
    def __init__(self):
        self.mode = None
        self.server = Server() # start the TCP server

        # initialise the controller listener
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("❌ No joystick detected.")
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        print("🎮 Listening for button presses...")

    def run(self):

        self.server.start()

        print("[SUPERVISOR] Waiting for mode selection:")
        while self.mode == None:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.joystick.get_button(0):
                        print("[SUPERVISOR] Starting in TELEOP mode")
                        self.mode = "TELEOP"
                        self.server.command_queue.put("TELEOP START")
                    elif self.joystick.get_button(1):
                        print("[SUPERVISOR] Starting in AUTO mode")
                        self.mode = "AUTO"
                        self.server.command_queue.put("AUTONOMOUS START")

        while True:
            pygame.event.pump() # Update joystick state

            teleop_switch = self.joystick.get_button(0)
            auto_switch = self.joystick.get_button(1)

            if teleop_switch & (self.mode != "TELEOP"):
                self.server.command_queue.put("SWITCH TO TELEOP")
                self.mode = "TELEOP"
            elif auto_switch & (self.mode != "AUTO"):
                self.server.command_queue.put("SWITCH TO AUTONOMOUS")
                self.mode = "AUTO"

            #I would do it this way but up to you it would replace (62-70)
            # if event.type == pygame.JOYBUTTONDOWN and self.joystick.get_button(6):
            #     if self.mode != "TELEOP":
            #         self.server.command_queue.put("SWITCH TO TELEOP")
            #         self.mode = "TELEOP"
            #     else:
            #         self.server.command_queue.put("SWITCH TO AUTONOMOUS")
            #         self.mode = "AUTO"

            if self.mode == "TELEOP":
                x = self.joystick.get_axis(0)        # forward and reverse (Left Stick up and down)
                y = self.joystick.get_axis(1)        # strafe left and right (Left Stick left and right)
                yaw_rate = self.joystick.get_axis(2) # yaw angle rate (Right Stick left and right)
                if event.type == pygame.JOYBUTTONDOWN:
                    # I would also do this a toggle but up to you
                    # I dont know how using the same button on the same section of code would work
                    # They would both fire at the same time
                    start_mining_motor = self.joystick.get_button(4) # start mining belt motor (LB)
                    stop_mining_motor = self.joystick.get_button(5)  # stop mining belt motor (RB)
                    start_dumping_motor = self.joystick.get_axis(4)  # start mining belt motor (LT)
                    stop_dumping_motor = self.joystick.get_axis(5)   # stop mining belt motor (RT)

                self.commands = [x, y, yaw_rate, start_mining_motor, stop_mining_motor, start_dumping_motor, stop_dumping_motor]
                self.server.command_queue.put(self.commands)
                time.sleep(0.1)
            
            # print(f"[TELEOP] Joystick axes: x={x:.2f}, y={y:.2f}")
            # time.sleep(0.1)

if __name__ == "__main__":
    Supervisor().run()
