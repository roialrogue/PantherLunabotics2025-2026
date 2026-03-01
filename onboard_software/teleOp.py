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
                #Forward
                if robot_params.RobotConfig.useDrivetrain:
                    self.robot.drivetrain.set_power(-0.5,0.5,-0.5,0.5)
        elif button == 'B':
            if is_pressed:
                #strafe right
                if robot_params.RobotConfig.useDrivetrain:
                    self.robot.drivetrain.set_power(-0.5,0.5,0.5,-0.5)
        elif button == 'X':
            if is_pressed:
                #strafe left
                if robot_params.RobotConfig.useDrivetrain:
                    self.robot.drivetrain.set_power(0.5,-0.5,-0.5,0.5)
        elif button == 'Y':
            if is_pressed:
                #backward
                if robot_params.RobotConfig.useDrivetrain:
                    self.robot.drivetrain.set_power(0.5,-0.5,0.5,-0.5)
        elif button == 'LB':
            if is_pressed:
                #Turn left
                if robot_params.RobotConfig.useDrivetrain:
                    self.robot.drivetrain.set_power(-0.5,-0.5,-0.5,-0.5)
        elif button == 'RB':
            if is_pressed:
                #Turn right
                if robot_params.RobotConfig.useDrivetrain:
                    self.robot.drivetrain.set_power(0.5,0.5,0.5,0.5)
        elif button == 'DPAD_UP':
            if is_pressed:
                #Intake
                self.robot.auger.intake()
        elif button == 'DPAD_DOWN':
            if is_pressed:
                #Outtake
                self.robot.auger.outtake()
        elif button == 'DPAD_LEFT':
            if is_pressed:
                #Off
                if robot_params.RobotConfig.useDrivetrain:
                    self.robot.drivetrain.set_power(0.0,0.0,0.0,0.0)
        elif button == 'DPAD_RIGHT':
            if is_pressed:
                self.robot.auger.stop()

    """Called at 50Hz — put all periodic tasks here."""
    def periodic_loop(self):

        #if robot_params.RobotConfig.useDrivetrain:
        #    self.robot.drivetrain.drive_task(self.robot.controller.AxisValues['LY'], self.robot.controller.AxisValues['LX'], self.robot.controller.AxisValues['RX'])
        
        # Update motor controller
        try:
            self.robot.motor_controller.update()
        except RuntimeError:
            pass

    def run_teleOp_step(self):

        # Update periodic loop
        now = time.monotonic()
        elapsed = now - self._last_update_time
        if elapsed >= robot_params.LoopConfig.UPDATE_PERIOD_S:
            self.periodic_loop()
            self._last_update_time = now
