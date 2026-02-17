# RobotParams
# Stores all constants and configs used acrooss the robot codebase.

class LoopConfig:
    UPDATE_RATE_HZ = 50  # Change this to adjust loop frequency
    UPDATE_PERIOD_S = 1.0 / UPDATE_RATE_HZ  # 0.02s at 50Hz