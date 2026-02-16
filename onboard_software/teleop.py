from __future__ import annotations
import robot


class TeleOp:
    def __init__(self, robot: robot.Robot):
        self.robot = robot

    # Called only when there is a button event
    def on_button_event(self, button, is_pressed):
        if button == 'A':
            if is_pressed:
                #Full reverse
                self.robot.drivetrain.set_power(-0.5,-0.5,-0.5,-0.5)
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
                self.robot.drivetrain.set_power(0.5,-0.5,-0.5,0.5)
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

    def run_teleOp_step(self):
        pass

        #self.robot.drivetrain.drive_task(self.robot.controller.AxisValues['LY'], self.robot.controller.AxisValues['LX'], self.robot.controller.AxisValues['RX'])