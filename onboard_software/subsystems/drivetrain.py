import math
from library.util import Util
import motor_controller

class Drivetrain:

    def __init__(self, mc):
        self.slow_turning = True
        self.max_speed = 0.1

        self.mc = mc
        self.motor_ids = [1, 2, 3, 4] # Example motor IDs for a 4-motor drivetrain

        config = motor_controller.MotorConfig()
        config.idle_mode = motor_controller.IdleMode.BRAKE
        config.motor_type = motor_controller.MotorType.BRUSHLESS
        config.sensor_type = motor_controller.SensorType.HALL_SENSOR
        config.ramp_rate = 0.0
        config.inverted = False
        config.motor_kv = 480
        config.encoder_counts_per_rev = 4096
        config.smart_current_free_limit = 20.0
        config.smart_current_stall_limit = 80.0

        self.mc.initialize_motors(self.motor_ids, config)

    def set_slow_turning(self, slow_turning):
        self.slow_turning = slow_turning

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def set_power(self, front_right_power, front_left_power, back_right_power, back_left_power):
        self.mc.set_motor_duty_cycle(self.motor_ids[0], Util.clip(front_right_power, -self.max_speed, self.max_speed))
        self.mc.set_motor_duty_cycle(self.motor_ids[1], Util.clip(front_left_power, -self.max_speed, self.max_speed))
        self.mc.set_motor_duty_cycle(self.motor_ids[2], Util.clip(back_right_power, -self.max_speed, self.max_speed))
        self.mc.set_motor_duty_cycle(self.motor_ids[3], Util.clip(back_left_power, -self.max_speed, self.max_speed))

    def drive_task(self, y_axis, x_axis, turning_axis):
        y = -(math.atan(5 * y_axis) / math.atan(5))
        x = (math.atan(5 * x_axis) / math.atan(5)) * 1.1 # Strafing compensation
        turning = (math.atan(5 * turning_axis) / math.atan(5))

        if self.slow_turning:
            turning *= 0.5 # Slow down turning

        denominator = max(abs(y) + abs(x) + abs(turning), 1)
        front_right_power = (y - x - turning) / denominator
        front_left_power = (y + x + turning) / denominator
        back_right_power = (y + x - turning) / denominator
        back_left_power = (y - x + turning) / denominator

        self.set_power(front_right_power, front_left_power, back_right_power, back_left_power)

    def stop(self):
        self.set_power(0, 0, 0, 0)
