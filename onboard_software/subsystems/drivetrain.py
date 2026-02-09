import math
from library.util import Util

class Drivetrain:

    def __init__(self, mc):
        self.slow_turning = True
        self.max_speed = 1.0

        self.mc = mc
        self.motor_ids = [1, 2, 3, 4] # Example motor IDs for a 4-motor drivetrain

        config = mc.MotorConfig()
        config.idle_mode = mc.IdleMode.BRAKE
        config.motor_type = mc.MotorType.BRUSHLESS
        config.sensor_type = mc.SensorType.HALL_SENSOR
        config.ramp_rate = 0.1
        config.inverted = False
        config.motor_kv = 560
        config.encoder_counts_per_rev = 7168
        config.smart_current_free_limit = 20.0
        config.smart_current_stall_limit = 20.0

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
