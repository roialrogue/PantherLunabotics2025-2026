from __future__ import annotations
import robot


class Auto:
    def __init__(self, robot: robot.Robot):
        self.robot = robot

    # Called only when there is a button event
    def on_button_event(self, button, is_pressed):
        if button == 'A':
            if is_pressed:
                print("[AUTO] A button pressed")
            else:
                print("[AUTO] A button released")
        elif button == 'B':
            if is_pressed:
                print("[AUTO] B button pressed")
            else:
                print("[AUTO] B button released")
        elif button == 'X':
            if is_pressed:
                print("[AUTO] X button pressed")
            else:
                print("[AUTO] X button released")
        elif button == 'Y':
            if is_pressed:
                print("[AUTO] Y button pressed")
            else:
                print("[AUTO] Y button released")
        elif button == 'LB':
            if is_pressed:
                print("[AUTO] LB button pressed")
            else:
                print("[AUTO] LB button released")
        elif button == 'RB':
            if is_pressed:
                print("[AUTO] RB button pressed")
            else:
                print("[AUTO] RB button released")

    def run_auto_step(self):
        pass