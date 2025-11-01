import RPi.GPIO as GPIO
import library.pid_controller as Controller
import library.motor as Motor

class MotorExample: 
    def __init__(self):
        self.pid_coefficients = Controller.PIDController.PIDCoefficients(kp=0, ki=0, kd=0)
        self.pin = 33

        self.target_position = 0
        self.power_limit = 1.0

        # Subsystem constants
        self.power_limit = 1.0
        self.ticks_per_inch = 0 # Ticks moved / inches moved
        self.max_pos = 0 # Inches
        self.min_pos = 0 # Inches
        self.gravity_compensation_power = 0.0
        self.zero_position_offset = 0.0
        # If circle Ticks_Per_Degree = ENCODER_CPR * GEAR_RATIO / 360.0

        # Initialize GPIO pin and PID controller
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(self.pin, self.motor.get_frequency())
        self.controller = Controller.PIDController(self.pid_coefficients)
        self.motor = Motor.Motor()

    # This method is called periodically so that the PID controller can move the subsystem towards its target
    def motor_task(self):
        self.controller.setOutputLimit(self.power_limit)
        current_position = self.get_current_position()
        pidOutput = self.controller.calculate(current_position, self.target_position)
        power = self.gravity_compensation_power + pidOutput # For a straight linear system
        duty_cycle = self.motor.calculate_power(power)
        self.pwm.start(duty_cycle)
        print(f"Target: {self.target_position:.2f} | Current: {current_position:.2f} | Power: {power:.2f}")

    # Bypass all safety and set power directly
    # Will be removed after testing most likely
    def set_power(self, power):
        duty_cycle = self.motor.calculate_power(power)
        self.pwm.start(duty_cycle)

    def is_on_target(self, tolerance=1, timeout=0.0, no_oscillation=False):
        self.controller.setNoOscillation(no_oscillation)
        self.controller.setTimeout(timeout)
        return self.controller.isOnTarget(tolerance)
    
    def set_position(self, position, power_limit=1.0):
        self.target_position = position
        self.power_limit = power_limit

    def set_pid_power(self, power):
        if power > 0.0:
            self.set_position(self.max_pos, power)
        elif power < 0.0:
            self.set_position(self.min_pos, power)
        else:
            # Hold position
            self.set_position(self.get_real_world_position(), 1.0)

    # Get motor position in inches
    def get_current_position(self):
        # TODO: Implement encoder reading
        return 0.0

    # Offset the zero position by a given number of inches
    def get_real_world_position(self):
        return self.get_current_position() + self.zero_position_offset

    def cleanup_motor(self):
        self.pwm.stop()
        GPIO.cleanup()