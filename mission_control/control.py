import time
import pygame
import client as client

'''
Axis 0 - Left Stick (L = -1, R = 1)
Axis 1 - Left Stick (T = -1, D = 1)
Axis 2 - Right Stick (L = -1, R = 1)
Axis 3 - Right Stick (T = -1, D = 1)

Axis 4 - Left Trigger (unpressed = -1, pressed = 1)
Axis 5 - Right Trigger (unpressed = -1, pressed = 1)

Button 0 - A
Button 1 - B
Button 2 - X
Button 3 - Y
Button 4 - LB
Button 5 - RB
Button 6 - Options
Button 7 - Start
'''

class Control:
    def __init__(self, server_ip):
        self.running = True
        self.mode = None
        #self.client = client.Client(server_ip) # start the TCP server

        # initialise the controller listener
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("❌ No joystick detected.")
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print("🎮 Listening for controller action...")

    def run(self):
        #self.client.connect()

        print("[Control] Waiting for mode selection: \n Press A for TELEOP \n Press B for AUTO")
        while self.mode == None:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    button = event.button
                    if button == 0:
                        print("[Control] Starting in TELEOP mode")
                        self.mode = "TELEOP"
                    elif button == 1:
                        print("[Control] Starting in AUTO mode")
                        self.mode = "AUTO"

        # Prevent A/B release events from leaking into control loop
        while self.joystick.get_button(0) or self.joystick.get_button(1):
            pygame.event.pump()
            time.sleep(0.05)
        pygame.event.clear()
        
        button_map = {
            "A": 0,
            "B": 1,
            "X": 2,
            "Y": 3,
            "LB": 4,
            "RB": 5
        }
        last_command = None

        while self.running:
            pygame.event.pump() # Update joystick state

            # Read joystick axes
            x = self.joystick.get_axis(0)          # Left Stick up and down
            y = self.joystick.get_axis(1)          # Left Stick left and right
            yaw_rate = self.joystick.get_axis(2)   # Right Stick left and right
            pitch_rate = self.joystick.get_axis(3) # Right Stick up and down

            lt = self.joystick.get_axis(4)  # Left Trigger
            rt = self.joystick.get_axis(5)  # Right Trigger

            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:

                    if event.button == 7:
                        print("[Control] Stopping robot!")
                        self.stop()

                    # Toggle
                    if event.button == 6:
                        self.mode = "TELEOP" if self.mode != "TELEOP" else "AUTO"
                        print(f"[Control] Switching to {self.mode} mode")

                    for name, btn in button_map.items():
                        if event.button == btn:
                            # Button just pressed
                            buttonCommand = (self.mode, f"{name}_PRESSED")
                            #self.client.send_command(buttonCommand)
                            print(buttonCommand)

                elif event.type == pygame.JOYBUTTONUP:
                    for name, btn in button_map.items():
                        if event.button == btn:
                            # Button just released
                            buttonCommand = (self.mode, f"{name}_RELEASED")
                            #self.client.send_command(buttonCommand)
                            print(buttonCommand)

            commands = (self.mode, x, y, yaw_rate, pitch_rate, lt, rt)
            if commands != last_command:
                #self.client.send_command(commands)
                last_command = commands
                print(f"[Control] Sent command: {commands}")
            time.sleep(0.05)  # 20 Hz update rate

    def stop(self):
        self.running = False
        self.client.stop()

if __name__ == "__main__":
    server_ip = "localhost"  # Replace with the robot server's IP address
    Control(server_ip).run()
