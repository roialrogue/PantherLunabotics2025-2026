from __future__ import annotations
import robot


class TeleOp:
    def __init__(self, robot: robot.Robot):
        self.robot = robot

    # Called only when there is a button event
    def on_button_event(self, button, is_pressed):
        if button == 'A':
            if is_pressed:
                print("[TELEOP] A button pressed")
            else:
                print("[TELEOP] A button released")
        elif button == 'B':
            if is_pressed:
                print("[TELEOP] B button pressed")
            else:
                print("[TELEOP] B button released")
        elif button == 'X':
            if is_pressed:
                print("[TELEOP] X button pressed")
            else:
                print("[TELEOP] X button released")
        elif button == 'Y':
            if is_pressed:
                print("[TELEOP] Y button pressed")
            else:
                print("[TELEOP] Y button released")
        elif button == 'LB':
            if is_pressed:
                print("[TELEOP] LB button pressed")
            else:
                print("[TELEOP] LB button released")
        elif button == 'RB':
            if is_pressed:
                print("[TELEOP] RB button pressed")
            else:
                print("[TELEOP] RB button released")

    def run_teleOp_step(self):
        pass

        # Telemetry can not be run in this loop to low frequency (clogs up client server coms)
        # joystick_values = self.robot.controller.AxisValues.__str__()
        # self.robot.print_telemetry(f"Joystick values: {joystick_values}")