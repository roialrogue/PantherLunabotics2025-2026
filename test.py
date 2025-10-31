import rev

# Create a CANSparkMax object for your motor
device_id = 1  # CAN ID of your SPARK MAX
motor = rev.CANSparkMax(device_id, rev.CANSparkLowLevel.MotorType.kBrushless)

# Get the built-in encoder (for NEO motors)
encoder = motor.getEncoder()

# Read the position in rotations
position = encoder.getPosition()
print(f"Motor position: {position:.2f} rotations")
