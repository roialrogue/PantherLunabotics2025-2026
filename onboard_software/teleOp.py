from __future__ import annotations
import time
import robot_params
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import robot

class TeleOp:

    def __init__(self, robot: robot.Robot):
        self.robot = robot
        self._last_update_time = time.monotonic()

    # Called only when there is a button event
    def on_button_event(self, button, is_pressed):
        if button == 'A':
            if is_pressed:
                #All postive power
                self.robot.drivetrain.set_power(0.5,-0.5,0.5,-0.5)
                print("[TELEOP] A button pressed")
            else:
                print("[TELEOP] A button released")
        elif button == 'B':
            if is_pressed:
                #Turn left
                self.robot.drivetrain.set_power(-0.5,0.5,-0.5,0.5)
                print("[TELEOP] B button pressed")
            else:
                print("[TELEOP] B button released")
        elif button == 'X':
            if is_pressed:
                #Turn left
                self.robot.drivetrain.set_power(0.5,-0.5,0.5,-0.5)
                print("[TELEOP] X button pressed")
            else:
                print("[TELEOP] X button released")
        elif button == 'Y':
            if is_pressed:
                #Full foward
                self.robot.drivetrain.set_power(0.5,0.5,0.5,0.5)
                print("[TELEOP] Y button pressed")
            else:
                print("[TELEOP] Y button released")
        elif button == 'LB':
            if is_pressed:
                #Strafe left
                self.robot.drivetrain.set_power(0.0,0.0,0.0,0.0)
                #self.robot.drivetrain.set_power(0.5,-0.5,-0.5,0.5)
                print("[TELEOP] LB button pressed")
            else:
                print("[TELEOP] LB button released")
        elif button == 'RB':
            if is_pressed:
                #Strafe right
                self.robot.drivetrain.set_power(-0.5,0.5,0.5,-0.5)
                print("[TELEOP] RB button pressed")
            else:
                print("[TELEOP] RB button released")

    """Called at 50Hz — put all periodic tasks here."""
    def periodic_loop(self):

        #self.robot.drivetrain.set_power(0.1, 0.1, 0.1, 0.1)
        #self.robot.drivetrain.drive_task(self.robot.controller.AxisValues['LY'], self.robot.controller.AxisValues['LX'], self.robot.controller.AxisValues['RX'])
        
        # Update motor controller
        self.robot.motor_controller.update()

    def run_teleOp_step(self):

        # Update periodic loop
        now = time.monotonic()
        elapsed = now - self._last_update_time
        if elapsed >= robot_params.LoopConfig.UPDATE_PERIOD_S:
            self.periodic_loop()
            self._last_update_time = now
