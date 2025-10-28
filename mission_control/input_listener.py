import pygame
import threading
import time

class InputListener:
    def __init__(self):
        self.mode_callback = None
        self.running = False

    def set_callback(self, func):
        self.mode_callback = func

    def start(self):
        self.running = True
        # t = threading.Thread(target=self._run, daemon=True)
        # t.start()

    def _run(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("❌ No joystick detected.")
            return

        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        print("🎮 Listening for button presses...")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if joystick.get_button(0):
                        print("[INPUT] A button pressed — toggling mode")
                        if self.mode_callback:
                            self.mode_callback()
            time.sleep(0.05)
