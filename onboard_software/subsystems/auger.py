import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../library/motor_controller/build'))
import motor_controller # type: ignore

class Auger:

    def __init__(self, mc):
        self.mc = mc
        self.motor_id = 1

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

        self.mc.initialize_motor(self.motor_id, config)

    def set_power(self, power):
        self.mc.set_motor_duty_cycle(self.motor_id, power)

    def intake(self):
        self.set_power(0.5)

    def outtake(self):
        self.set_power(-0.5)
