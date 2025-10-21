import pygame 
import time

def main(mode, running, pygame):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    mode = "autonomous"
                elif event.button == 1:
                    mode = "manual"
                elif event.button == 7:
                    running = False
                
        if mode == "autonomous":
            print("Handoff to Autonomous control")
        elif mode == "manual":
            print("Manual Control Takeover")

if __name__ == "__main__":
    mode = "autonomous"
    running = True

    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)  # Get the first joystick
        joystick.init()
        print(f"Joystick: {joystick.get_name()} Successfully detected.")
    main(mode, running, pygame)