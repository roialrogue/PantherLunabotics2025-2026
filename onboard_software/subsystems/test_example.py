import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../library/motor_controller/build'))
try:
    import motor_controller as mc
except ImportError as e:
    print(f"ERROR: Failed to import motor_controller module: {e}")
    print("Make sure the module is compiled and the path is correct")
    sys.exit(1)

    def test_example(self):
        
        self.mc = mc.MotorController.get_instance("can0")
        self.motor_ids = 1

        config = mc.MotorConfig()
        config.idle_mode = mc.IdleMode.BRAKE
        config.motor_type = mc.MotorType.BRUSHLESS
        config.sensor_type = mc.SensorType.HALL_SENSOR
        config.ramp_rate = 0.0
        config.inverted = False
        config.motor_kv = 480
        config.encoder_counts_per_rev = 4096
        config.smart_current_free_limit = 20.0
        config.smart_current_stall_limit = 80.0

        self.mc.initialize_motor(self.motor_ids, config)

        print("Running motor at 50% power for 2 seconds...")
        start_time = time.time()
        while time.time() - start_time < 5:
            if time.time() - start_time < 2:
                self.mc.set_motor_duty_cycle(self.motor_ids, 0.1)
            elif time.time() - start_time < 4:
                self.mc.set_motor_duty_cycle(self.motor_ids, -0.1)
            else:
                self.mc.set_motor_duty_cycle(self.motor_ids, 0.0)
        print("Motor test complete.")

if __name__ == "__main__":
    test = test_example()