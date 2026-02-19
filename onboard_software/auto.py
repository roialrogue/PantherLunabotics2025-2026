from __future__ import annotations
import time
import robot_params
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import robot

class Auto:

    def __init__(self, robot: robot.Robot):
        self.robot = robot
        self._last_update_time = time.monotonic()

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

    """Called at 50Hz — put all periodic tasks here."""
    def periodic_loop(self):

        # Update motor controller
        robot.mc.update()

    def run_auto_step(self):

        # Update periodic loop
        now = time.monotonic()
        elapsed = now - self._last_update_time
        if elapsed >= robot_params.LoopConfig.UPDATE_PERIOD_S:
            self.periodic_loop()
            self._last_update_time = now
