import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../library/motor_controller/build'))
import motor_controller # type: ignore

class Auger:

    def __init__(self, mc):
        self.mc = mc
        self.motor_id = 3
        self._last_telemetry_time = 0.0

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
        self.set_power(0.25)

    def outtake(self):
        self.set_power(-0.25)

    def stop(self):
        self.set_power(0.0)

    def print_telemetry(self, duty_cycle=True, velocity=True, position=True, current=True, temperature=True, voltage=True, interval=0.1):
        now = time.monotonic()
        if now - self._last_telemetry_time < interval:
            return
        self._last_telemetry_time = now

        feedback = self.mc.get_motor_feedback(self.motor_id)

        parts = []
        if duty_cycle:
            parts.append(f"Duty Cycle: {feedback.duty_cycle:.4f}")
        if velocity:
            parts.append(f"Velocity: {feedback.velocity:.2f} RPM")
        if position:
            parts.append(f"Position: {feedback.position:.1f} ticks")
        if current:
            parts.append(f"Current: {feedback.current:.2f} A")
        if temperature:
            parts.append(f"Temp: {feedback.temperature:.1f} °C")
        if voltage:
            parts.append(f"Bus: {feedback.voltage:.2f} V")

        if not parts:
            return

        print("[Auger] " + ", ".join(parts))
