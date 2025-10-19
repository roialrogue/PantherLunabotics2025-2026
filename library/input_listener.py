import pygame
import threading

class InputListener:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.mode_callback = None  # function to call when button is pressed

    def set_callback(self, func):
        self.mode_callback = func

    def start(self):
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    # Assuming 'A' button is index 0
                    if event.button == 0 and self.mode_callback:
                        print("[INPUT] A button pressed — toggling mode")
                        self.mode_callback()
